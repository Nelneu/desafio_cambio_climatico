import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from scripts.prepare_delivery_package import plan, prepare, pdf_bytes


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.repo, self.package, self.intermediate, self.backup = [base / x for x in ('repo', 'package', 'intermediate', 'backup')]
        self.repo.mkdir()
        self.package.mkdir()
        self.intermediate.mkdir()
        # The fixture uses the real curated text, not dummy metric claims.
        real = Path(__file__).resolve().parents[1]
        for name in ('docs/executive-summary.md', 'docs/neural-validation.md', 'requirements.txt'):
            dest = self.repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((real / name).read_bytes())
        from scripts.prepare_delivery_package import COPY_MAP
        for source, _ in COPY_MAP:
            dest = self.repo / source
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(b'source ' + source.encode())
        for name in ('resultados_modelos_etapa3.csv', 'resultados_paso_4_1_mlp_regresion.csv'):
            (self.intermediate / name).write_text('model,result\nMLP,1\n')

    def test_plan_dry_run_and_rollback(self):
        unrelated = self.package / 'historical.html'
        unrelated.write_bytes(b'untouched')
        existing = self.package / 'etapa_1_EDA/01_EDA_completo.ipynb'
        existing.parent.mkdir()
        existing.write_bytes(b'original')
        before = {p.relative_to(self.package): p.read_bytes() for p in self.package.rglob('*') if p.is_file()}
        manifest = plan(self.repo, self.package, self.intermediate, self.backup)
        names = {x['destination'] for x in manifest['files']}
        self.assertEqual(len(names), 24)
        self.assertIn('resumen_ejecutivo.pdf', names)
        self.assertIn('datos/intermedios/resultados_modelos_etapa3.csv', names)
        self.assertNotIn('historical.html', names)
        self.assertFalse(self.backup.exists())
        self.assertEqual(before, {p.relative_to(self.package): p.read_bytes() for p in self.package.rglob('*') if p.is_file()})
        with self.assertRaises(RuntimeError):
            prepare(self.repo, self.package, self.intermediate, self.backup, apply=True,
                    fail_after=1)
        self.assertEqual(before, {p.relative_to(self.package): p.read_bytes() for p in self.package.rglob('*') if p.is_file()})
        self.assertEqual(unrelated.read_bytes(), b'untouched')
        record = json.loads((self.backup / 'manifest.json').read_text())
        collision = next(x for x in record['files'] if x['destination'] == str(existing.relative_to(self.package)))
        self.assertEqual(collision['original_sha256'], hashlib.sha256(b'original').hexdigest())
        self.assertEqual((self.backup / collision['backup']).read_bytes(), b'original')
        # Fail after the first created CSV: rollback removes both it and its new directories.
        second_backup = Path(self.tmp.name) / 'second-backup'
        with self.assertRaises(RuntimeError):
            prepare(self.repo, self.package, self.intermediate, second_backup, apply=True,
                    fail_after=11)
        self.assertEqual(before, {p.relative_to(self.package): p.read_bytes() for p in self.package.rglob('*') if p.is_file()})
        self.assertFalse((self.package / 'datos').exists())

    def test_promotion_uses_sibling_replace_after_manifest_and_backups(self):
        existing = self.package / 'etapa_1_EDA/01_EDA_completo.ipynb'
        existing.parent.mkdir()
        existing.write_bytes(b'original')
        from scripts.prepare_delivery_package import os as package_os
        real_replace = package_os.replace
        replacements = []

        def observe(src, dest):
            src, dest = Path(src), Path(dest)
            self.assertEqual(src.parent, dest.parent)
            self.assertTrue((self.backup / 'manifest.json').is_file())
            self.assertEqual((self.backup / 'originals/etapa_1_EDA/01_EDA_completo.ipynb').read_bytes(), b'original')
            replacements.append((src, dest))
            return real_replace(src, dest)

        with patch('scripts.prepare_delivery_package.os.replace', side_effect=observe):
            prepare(self.repo, self.package, self.intermediate, self.backup, apply=True)
        self.assertEqual(len(replacements), 24)
        self.assertFalse(any(p.name.startswith('.01_EDA_completo') for p in existing.parent.iterdir()))

    def test_failed_promotion_preserves_old_and_cleans_sibling(self):
        existing = self.package / 'etapa_1_EDA/01_EDA_completo.ipynb'
        existing.parent.mkdir()
        existing.write_bytes(b'original')
        from scripts.prepare_delivery_package import shutil as package_shutil
        real_copy = package_shutil.copyfile

        def fail_after_temp_write(src, dst):
            real_copy(src, dst)
            self.assertEqual(existing.read_bytes(), b'original')
            raise OSError('injected interrupted temporary copy')

        with patch('scripts.prepare_delivery_package.shutil.copyfile', side_effect=fail_after_temp_write):
            with self.assertRaisesRegex(OSError, 'injected interrupted temporary copy'):
                prepare(self.repo, self.package, self.intermediate, self.backup, apply=True)
        self.assertEqual(existing.read_bytes(), b'original')
        self.assertEqual(list(existing.parent.iterdir()), [existing])
        self.assertTrue((self.backup / 'manifest.json').is_file())

    def test_failed_replace_leaves_new_destination_absent_and_no_temporary(self):
        target = self.package / 'etapa_1_EDA/01_EDA_completo.ipynb'
        with patch('scripts.prepare_delivery_package.os.replace', side_effect=OSError('injected replace failure')):
            with self.assertRaisesRegex(OSError, 'injected replace failure'):
                prepare(self.repo, self.package, self.intermediate, self.backup, apply=True)
        self.assertFalse(target.exists())
        self.assertFalse(target.parent.exists())
        self.assertTrue((self.backup / 'manifest.json').is_file())

    def test_rollback_restoration_is_atomic_for_existing_file(self):
        existing = self.package / 'etapa_1_EDA/01_EDA_completo.ipynb'
        existing.parent.mkdir()
        existing.write_bytes(b'original')
        from scripts.prepare_delivery_package import os as package_os
        real_replace = package_os.replace
        states = []

        def observe(src, dst):
            dst = Path(dst)
            if dst == existing:
                states.append((Path(src).parent, existing.read_bytes()))
            return real_replace(src, dst)

        with patch('scripts.prepare_delivery_package.os.replace', side_effect=observe):
            with self.assertRaisesRegex(RuntimeError, 'injected promotion failure'):
                prepare(self.repo, self.package, self.intermediate, self.backup, apply=True, fail_after=1)
        self.assertEqual(states, [(existing.parent, b'original'), (existing.parent, b'source 01_EDA/01_EDA_completo.ipynb')])
        self.assertEqual(existing.read_bytes(), b'original')
        self.assertEqual(list(existing.parent.iterdir()), [existing])

    def test_pdf_wrap_and_page_height(self):
        pdf = pdf_bytes(['palabra ' * 140, 'X' * 180] * 18)
        streams = re.findall(rb'stream\n(.*?)\nendstream', pdf, re.S)
        self.assertGreater(len(streams), 1)
        for stream in streams:
            rendered = re.findall(rb'^\((.*)\) Tj T\*$', stream, re.M)
            self.assertLessEqual(len(rendered), 43)
            self.assertTrue(rendered)
            self.assertTrue(all(len(line.decode('cp1252')) <= 72 for line in rendered))

    def test_success_documents_and_exact_readback(self):
        manifest = prepare(self.repo, self.package, self.intermediate, self.backup, apply=True)
        for entry in manifest['files']:
            data = (self.package / entry['destination']).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (entry['size'], entry['sha256']))
        docx = self.package / 'resumen_ejecutivo.docx'
        with zipfile.ZipFile(docx) as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn('[Content_Types].xml', archive.namelist())
            ET.fromstring(archive.read('_rels/.rels'))
            xml = ET.fromstring(archive.read('word/document.xml'))
            text = ' '.join(t.text or '' for t in xml.iter() if t.tag.endswith('}t'))
        pdf = (self.package / 'resumen_ejecutivo.pdf').read_bytes()
        self.assertTrue(pdf.startswith(b'%PDF-1.4'))
        match = re.search(rb'startxref\n(\d+)\n%%EOF', pdf)
        self.assertIsNotNone(match)
        self.assertTrue(pdf[int(match.group(1)):].startswith(b'xref\n'))
        streams = re.findall(rb'stream\n(.*?)\nendstream', pdf, re.S)
        self.assertTrue(streams)
        pdf_text = ' '.join(line.decode('cp1252') for stream in streams
                            for line in re.findall(rb'^\((.*)\) Tj T\*$', stream, re.M))
        for phrase in ('16 países', '0.9264', '20.43', 'Excel originales', 'HTML existentes'):
            self.assertIn(phrase, text)
            self.assertIn(phrase, pdf_text)

    def test_reject_unsafe_paths_and_unavailable_inputs(self):
        from scripts.prepare_delivery_package import safe_path
        with self.assertRaises(ValueError):
            safe_path(self.package, '../outside')
        (self.package / 'etapa_1_EDA').mkdir()
        (self.package / 'etapa_1_EDA/01_EDA_completo.ipynb').symlink_to(self.repo / 'requirements.txt')
        with self.assertRaises(ValueError):
            plan(self.repo, self.package, self.intermediate, self.backup)
        (self.package / 'etapa_1_EDA/01_EDA_completo.ipynb').unlink()
        (self.intermediate / 'resultados_modelos_etapa3.csv').unlink()
        with self.assertRaises(ValueError):
            plan(self.repo, self.package, self.intermediate, self.backup)
        self.assertFalse(self.backup.exists())


if __name__ == '__main__':
    unittest.main()
