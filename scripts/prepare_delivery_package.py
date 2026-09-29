#!/usr/bin/env python3
"""Explicit, non-mirroring delivery transaction. --dry-run is the default."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import textwrap
import zipfile
from xml.sax.saxutils import escape


COPY_MAP = (
    ('01_EDA/01_EDA_completo.ipynb', 'etapa_1_EDA/01_EDA_completo.ipynb'),
    ('02_Limpieza/02_limpieza_transformacion.ipynb', 'etapa_2_ETL/02_limpieza_transformacion.ipynb'),
    ('03_Modelado_ML/03_modelado_ml.ipynb', 'etapa_3_Modelos_ML/03_modelado_ML.ipynb'),
    *((f'04_Redes_Neuronales/04_redes_neuronales_paso4_{part}.ipynb',
        f'etapa_4_Redes_Neuronales/04_redes_neuronales_paso4_{part}.ipynb')
      for part in ('1', '2', '3', '4_A', '4_B', '4_C')),
    ('05_Storytelling/05_informe_final.ipynb', 'etapa_5_Storytelling/05_informe_final_storytelling.ipynb'),
    *((f'datos/limpios/{name}.csv', f'datos/limpios/{name}.csv') for name in (
        'dataset_argentina_anual', 'dataset_argentina_mensual',
        'dataset_argentina_provincias', 'dataset_argentina_provincias_wide', 'dataset_global')),
    ('requirements.txt', 'requirements.txt'),
    ('docs/neural-validation.md', 'docs/neural-validation.md'),
    ('docs/executive-summary.md', 'docs/executive-summary.md'),
)
INTERMEDIATES = ('resultados_modelos_etapa3.csv', 'resultados_paso_4_1_mlp_regresion.csv')
OUTPUTS = ('README.md', 'datos/originales/README.md', 'resumen_ejecutivo.docx', 'resumen_ejecutivo.pdf')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, relative=''):
    """Reject lexical escapes and symlinks in every existing component, including root."""
    if '..' in Path(root).parts:
        raise ValueError(f'unsafe root path: {root}')
    root = Path(os.path.abspath(root))
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError(f'unsafe relative path: {relative}')
    target = root / rel
    for path in (root, *root.parents, *(root / Path(*rel.parts[:i]) for i in range(1, len(rel.parts) + 1))):
        if path.is_symlink():
            raise ValueError(f'symlink not allowed: {path}')
    return target


def existing_bytes(root, relative):
    path = safe_path(root, relative)
    if not path.is_file():
        raise ValueError(f'missing or non-file source: {path}')
    return path.read_bytes()


def paragraphs(markdown):
    blocks = [block.strip() for block in markdown.split('\n\n') if block.strip()]
    if any('\n' in block or block.startswith(('-', '*', '|', '```')) for block in blocks):
        raise ValueError('summary format must be single-line headings and paragraphs')
    return [block.lstrip('# ').strip() for block in blocks]


def docx_bytes(blocks):
    body = ''.join('<w:p><w:pPr><w:spacing w:after="200"/></w:pPr><w:r><w:t xml:space="preserve">' +
                   escape(block) + '</w:t></w:r></w:p>' for block in blocks)
    document = ('<?xml version="1.0" encoding="UTF-8"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                '<w:body>' + body + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
                '<w:pgMar w:top="1200" w:right="1200" w:bottom="1200" w:left="1200"/>'
                '</w:sectPr></w:body></w:document>')
    parts = {
        '[Content_Types].xml': '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>',
        '_rels/.rels': '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>',
        'word/document.xml': document,
    }
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as archive:
        for name, value in parts.items():
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, value.encode('utf-8'))
    return out.getvalue()


def pdf_bytes(blocks):
    lines = []
    for block in blocks:
        lines.extend(textwrap.wrap(block, width=72, break_long_words=True))
        lines.append('')
    pages = [lines[i:i + 43] for i in range(0, len(lines), 43)]
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>', b'', b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>']
    kids = []
    for page in pages:
        page_id = len(objects) + 1
        stream_id = page_id + 1
        kids.append(f'{page_id} 0 R')
        stream = ['BT /F1 11 Tf 50 790 Td 14 TL']
        for line in page:
            value = line.encode('cp1252').decode('latin1')
            value = value.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
            stream.append(f'({value}) Tj T*')
        stream.append('ET')
        data = '\n'.join(stream).encode('latin1')
        objects.extend([f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {stream_id} 0 R >>'.encode(),
                        f'<< /Length {len(data)} >>\nstream\n'.encode() + data + b'\nendstream'])
    objects[1] = f'<< /Type /Pages /Kids [{" ".join(kids)}] /Count {len(kids)} >>'.encode()
    out = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(out))
        out.extend(f'{i} 0 obj\n'.encode() + obj + b'\nendobj\n')
    start = len(out)
    out.extend(f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]:
        out.extend(f'{offset:010d} 00000 n \n'.encode())
    out.extend(f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode())
    return bytes(out)


def generated(repo):
    summary = paragraphs(existing_bytes(repo, 'docs/executive-summary.md').decode('utf-8'))
    notebooks = '\n'.join(f'- `{dst}`' for src, dst in COPY_MAP if dst.endswith('.ipynb'))
    readme = ('# Entregables DPDS\n\nNotebooks fuente incluidos:\n' + notebooks +
              '\n\nDatos procesados: `datos/limpios/`; resultados medidos: `datos/intermedios/`. '
              'Documento: `resumen_ejecutivo.pdf` o `.docx`. Evidencia: `docs/neural-validation.md`. '
              'Para ejecutar desde esta raíz, usar `requirements.txt` y los CSV incluidos. '
              'Etapa 2 exige libros originales ausentes; ver `datos/originales/README.md`. '
              'Los HTML existentes son instantáneas históricas, no se actualizan y pueden mostrar cifras o rutas obsoletas. '
              'Los outputs guardados en notebooks también pueden ser históricos.\n')
    originals = ('# Fuentes originales no incluidas\n\nLos cinco libros Excel originales no están en esta entrega. '
                 'Los CSV procesados permiten leer análisis posteriores, pero no reproducir la limpieza ETL desde datos crudos. '
                 'No se afirma procedencia ni permiso de distribución de los libros.\n')
    return {'README.md': readme.encode(), 'datos/originales/README.md': originals.encode(),
            'resumen_ejecutivo.docx': docx_bytes(summary), 'resumen_ejecutivo.pdf': pdf_bytes(summary)}


def inventory(repo, package, intermediate, backup):
    roots = [safe_path(p) for p in (repo, package, intermediate, backup)]
    repo, package, intermediate, backup = roots
    if not repo.is_dir() or not package.is_dir() or not intermediate.is_dir():
        raise ValueError('repo, package and intermediate roots must exist as directories')
    if backup == package or backup in package.parents or package in backup.parents:
        raise ValueError('backup and package roots must not intersect')
    if backup.exists() and (not backup.is_dir() or any(backup.iterdir())):
        raise ValueError('backup root must be absent or empty')
    staged = {}
    for source, destination in COPY_MAP:
        staged[destination] = existing_bytes(repo, source)
    for name in INTERMEDIATES:
        staged[f'datos/intermedios/{name}'] = existing_bytes(intermediate, name)
    staged.update(generated(repo))
    if len(staged) != len(COPY_MAP) + len(INTERMEDIATES) + len(OUTPUTS):
        raise ValueError('duplicate destination')
    files = []
    for name, data in staged.items():
        dest = safe_path(package, name)
        if dest.exists() and not dest.is_file():
            raise ValueError(f'non-file destination: {dest}')
        old = dest.read_bytes() if dest.exists() else None
        files.append({'destination': name, 'sha256': digest(data), 'size': len(data),
                      'action': 'unchanged' if old == data else 'replace' if old is not None else 'create',
                      'original_sha256': digest(old) if old is not None else None,
                      'original_size': len(old) if old is not None else None})
    return staged, {'files': files, 'backup_root': str(backup), 'package_root': str(package),
                    'rollback': 'Restore backed-up collisions by path and remove only created allowlisted files; keep unrelated paths.'}


def plan(repo, package, intermediate, backup):
    return inventory(repo, package, intermediate, backup)[1]


def promote_file(source, destination):
    """Copy into a sibling, then replace one destination without exposing partial bytes."""
    fd, temporary = tempfile.mkstemp(prefix=f'.{destination.name}.', suffix='.tmp',
                                     dir=destination.parent)
    os.close(fd)
    temporary = Path(temporary)
    try:
        shutil.copyfile(source, temporary)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def prepare(repo, package, intermediate, backup, apply=False, fail_after=None):
    staged, manifest = inventory(repo, package, intermediate, backup)
    if not apply:
        return manifest
    package, backup = safe_path(package), safe_path(backup)
    backup.mkdir(parents=True, exist_ok=True)
    changes = [entry for entry in manifest['files'] if entry['action'] != 'unchanged']
    # Stage all outputs and all collision backups before the first destination write.
    for entry in changes:
        name = entry['destination']
        stage = safe_path(backup, 'staged/' + name)
        stage.parent.mkdir(parents=True, exist_ok=True)
        stage.write_bytes(staged[name])
        if digest(stage.read_bytes()) != entry['sha256']:
            raise IOError(f'stage readback failed: {name}')
        if entry['action'] == 'replace':
            original = safe_path(package, name).read_bytes()
            if digest(original) != entry['original_sha256']:
                raise IOError(f'collision changed: {name}')
            saved = safe_path(backup, 'originals/' + name)
            saved.parent.mkdir(parents=True, exist_ok=True)
            saved.write_bytes(original)
            if digest(saved.read_bytes()) != entry['original_sha256']:
                raise IOError(f'backup readback failed: {name}')
        entry['backup'] = 'originals/' + name if entry['action'] == 'replace' else None
    manifest_path = safe_path(backup, 'manifest.json')
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    promoted = []
    made_dirs = []
    try:
        for entry in changes:
            name = entry['destination']
            dest = safe_path(package, name)
            if entry['action'] == 'replace' and digest(dest.read_bytes()) != entry['original_sha256']:
                raise IOError(f'collision changed before promotion: {name}')
            if entry['action'] == 'create' and dest.exists():
                raise IOError(f'destination appeared: {name}')
            parents = []
            parent = dest.parent
            while parent != package and not parent.exists():
                parents.append(parent)
                parent = parent.parent
            for directory in reversed(parents):
                directory.mkdir()
                made_dirs.append(directory)
            promote_file(safe_path(backup, 'staged/' + name), dest)
            promoted.append(entry)
            if digest(dest.read_bytes()) != entry['sha256']:
                raise IOError(f'promotion readback failed: {name}')
            if fail_after is not None and len(promoted) >= fail_after:
                raise RuntimeError('injected promotion failure')
    except Exception:
        for entry in reversed(promoted):
            dest = safe_path(package, entry['destination'])
            if entry['action'] == 'replace':
                promote_file(safe_path(backup, entry['backup']), dest)
                if digest(dest.read_bytes()) != entry['original_sha256']:
                    raise IOError(f'ROLLBACK FAILED: {dest}')
            elif dest.exists():
                dest.unlink()
        for directory in reversed(made_dirs):
            directory.rmdir()
        raise
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--package-root', type=Path, required=True)
    parser.add_argument('--backup-root', type=Path, required=True)
    parser.add_argument('--intermediate-root', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        result = prepare(args.repo_root, args.package_root, args.intermediate_root, args.backup_root, apply=args.apply)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f'package transaction failed: {exc}\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
