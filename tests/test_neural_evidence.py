"""Source-facing DR-3 reconciliation; no model training or private data access."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def source(path):
    notebook = json.loads((ROOT / path).read_text(encoding='utf-8'))
    return '\n'.join(''.join(cell['source']) for cell in notebook['cells'])


class NeuralEvidence(unittest.TestCase):
    def test_style_dependency_is_direct(self):
        self.assertIn('jinja2>=3.1.5', (ROOT / 'requirements.txt').read_text())

    def test_protocol_and_metrics_documented(self):
        text = (ROOT / 'docs/neural-validation.md').read_text()
        for value in ('0.9796', '0.7349', '0.9264', '0.0103', '0.7568',
                      '20.43', '0.10', '72.75', '0.34', '107.93', '0.27',
                      '20.74', '26.68', '20.70', '3.47', '20.61',
                      '2017', '2018', '5e-4', '32', '2.21', '3.12'):
            with self.subTest(value=value):
                self.assertIn(value, text)
        self.assertIn('4.4.B', text)
        self.assertIn('no reproduce', text)

    def test_synthesis_uses_b_measures_not_tuned_43(self):
        text = source('04_Redes_Neuronales/04_redes_neuronales_paso4_4_C.ipynb')
        for fragment in ("'Valor': 0.9264, 'Desvío seeds': 0.0103",
                         "'Valor': 0.7568", "'Valor': 20.70, 'Desvío seeds': 3.47",
                         "'Valor': 20.61", 'alternativa histórica (4.4.B)',
                         '20.43', '4.3'):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_readme_does_not_infer_mlp_mechanism(self):
        text = (ROOT / '04_Redes_Neuronales/README.md').read_text()
        for unsupported in ('Hipótesis verificada empíricamente', 'Prueba contundente',
                            'las MLPs aprenden ratios implícitos',
                            'superioridad del deep learning no es magia',
                            'Diagnósticos de overfitting descartados'):
            with self.subTest(unsupported=unsupported):
                self.assertNotIn(unsupported.casefold(), text.casefold())
        self.assertIn('no demuestra', text)

    def test_synthesis_does_not_generalize_rankings_or_rules(self):
        text = source('04_Redes_Neuronales/04_redes_neuronales_paso4_4_C.ipynb')
        for unsupported in ('claramente superior', 'están dominados por Lasso',
                            'DL gana fuerte', 'no vas a perder casi nada',
                            'techo de mejora es bajísimo',
                            'superan claramente a ARIMA',
                            'la frontera incluye a', 'tuning fue caro y devolvió poco'):
            with self.subTest(unsupported=unsupported):
                self.assertNotIn(unsupported.casefold(), text.casefold())
        self.assertIn('solo en esta muestra', text)

    def test_storytelling_does_not_claim_quotient_discovery(self):
        text = source('05_Storytelling/05_informe_final.ipynb')
        self.assertNotIn('las redes neuronales pueden encontrar el cociente por uno', text)
        self.assertIn('no prueban que la red lo haya construido internamente', text)

    def test_cleaning_effort_has_no_unmeasured_percentage(self):
        text = source('05_Storytelling/05_informe_final.ipynb')
        self.assertNotIn('60% del esfuerzo', text)
        self.assertIn('trabajo de limpieza', text)

    def test_manual_feature_claim_keeps_protocols_separate(self):
        text = source('05_Storytelling/05_informe_final.ipynb')
        self.assertNotIn('un modelo lineal de 7 parámetros igualó la performance', text)
        self.assertNotIn('conviene siempre intentar features mejores', text)
        self.assertIn('4.1 y 4.4.A', text)
        self.assertIn('explorar ingeniería de variables', text)

    def test_longer_series_are_not_promised_to_improve(self):
        text = source('05_Storytelling/05_informe_final.ipynb')
        self.assertNotIn('podrían dar mejoras significativas', text)
        self.assertNotIn('se beneficiaría de más historia', text)
        self.assertIn('hipótesis no evaluada', text)

    def test_determinism_is_conditional_not_portability_proof(self):
        text = source('04_Redes_Neuronales/04_redes_neuronales_paso4_4_C.ipynb')
        self.assertNotIn('perfectamente reproducibles', text)
        self.assertNotIn('siempre dan el mismo resultado', text)
        self.assertIn('entorno, entradas y configuración', text)
        self.assertIn('no se verificó reproducibilidad entre plataformas', text)

    def test_43_conclusion_reports_observed_tradeoff_without_winner(self):
        notebook = json.loads((ROOT / '04_Redes_Neuronales/04_redes_neuronales_paso4_3.ipynb').read_text())
        conclusion = ''.join(notebook['cells'][39]['source'])
        for value in ('20.43', '20.74', '72.75', '70.87', '2018',
                      'sin prueba de superioridad estadística'):
            with self.subTest(value=value):
                self.assertIn(value, conclusion)
        for stale in ('21.75%', '18.24%', 'mejor opción defensible',
                      'estadísticamente indistinguible'):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, conclusion)

    def test_p1_recommendation_does_not_call_arima_performance_winner(self):
        notebook = json.loads((ROOT / '05_Storytelling/05_informe_final.ipynb').read_text())
        p1 = ''.join(notebook['cells'][3]['source'])
        self.assertNotIn('son suficientes y más fáciles de auditar', p1)
        self.assertIn('no fue el menor MAPE', p1)
        self.assertIn('auditabilidad', p1)

    def test_storytelling_separates_all_runs(self):
        text = source('05_Storytelling/05_informe_final.ipynb')
        for fragment in ('4.1', '0.9796', '0.7349', '4.4.A', '0.9264',
                         '0.7568', '4.3', '20.43', '20.74', '26.68',
                         '4.4.B', '20.70', '20.61'):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)
        self.assertIn('no reproduce', text)


if __name__ == '__main__':
    unittest.main()
