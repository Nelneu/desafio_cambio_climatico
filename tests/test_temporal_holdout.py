"""Contrato estático del holdout temporal de la etapa 4.3 (sin TensorFlow)."""
import ast
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / '04_Redes_Neuronales'


def celdas(nombre):
    return json.loads((BASE / nombre).read_text(encoding='utf-8'))['cells']


def codigo(nombre):
    return '\n'.join(''.join(c['source']) for c in celdas(nombre) if c['cell_type'] == 'code')


class HoldoutTemporal(unittest.TestCase):
    def test_separacion_y_escalado(self):
        src = codigo('04_redes_neuronales_paso4_3.ipynb')
        self.assertIn('ts_val = ts_train.iloc[-VAL_SIZE:]', src)
        self.assertIn('ts_tuning = ts_train.iloc[:-VAL_SIZE]', src)
        self.assertIn('scaler.fit_transform(ts_tuning.values.reshape(-1, 1))', src)
        self.assertIn('forecast_recursive_univariate(model, seed_window, n_steps, scaler_fwd)', src)

    def test_seleccion_no_usa_test(self):
        cells = celdas('04_redes_neuronales_paso4_3.ipynb')
        src = '\n'.join(''.join(c['source']) for c in cells[14:31] if c['cell_type'] == 'code')
        self.assertNotIn('ts_test', src)
        self.assertIsNone(re.search(r'\bmape_42\b|\bmape_arima\b', src))
        self.assertIn("best_bs = df_E4.loc[df_E4['MAPE validación (%)'].idxmin()", src)
        self.assertIn("best_lr = df_E5.loc[df_E5['MAPE validación (%)'].idxmin()", src)
        self.assertIn("best_reg_name = df_E6.loc[df_E6['MAPE validación (%)'].idxmin()", src)
        self.assertNotIn('MAPE (%)', src)

    def test_final_reentrena_y_test_solo_al_final(self):
        cells = celdas('04_redes_neuronales_paso4_3.ipynb')
        tuning = '\n'.join(''.join(c['source']) for c in cells[:32] if c['cell_type'] == 'code')
        final = '\n'.join(''.join(c['source']) for c in cells[32:] if c['cell_type'] == 'code')
        self.assertNotIn('ts_test.values', tuning)
        self.assertIn('ts_test.values', final)
        self.assertIn('scaler_final.fit_transform(ts_train.values.reshape(-1, 1))', final)
        self.assertIn('shuffle=False', final)

    def test_configuracion_historica_no_reclama_ganadores_actuales(self):
        texto = ''.join(celdas('04_redes_neuronales_paso4_4_B.ipynb')[17]['source'])
        self.assertIn('configuración histórica independiente', texto.lower())
        for valor in ('(ganador del E4)', '(ganador del E5)', '(ganador del E6)'):
            self.assertNotIn(valor, texto)

    def test_seed_ilustrativa_fijada_sin_consultar_mape_test(self):
        src = ''.join(celdas('04_redes_neuronales_paso4_4_B.ipynb')[25]['source'])
        previo = src.split('fig, ax =', 1)[0]
        namespace = {'SEEDS_TUNED': [42, 123, 7], 'corridas_tuneada': [
            {'seed': 42, 'MAPE': 99}, {'seed': 123, 'MAPE': 1}, {'seed': 7, 'MAPE': 20},
        ]}
        exec(compile(ast.parse(previo), '<selección de figura>', 'exec'), namespace)
        self.assertEqual(namespace['ilustrativa']['seed'], 42)
        self.assertNotIn("['MAPE']", previo)
        self.assertIn('ilustrativa', src)
        self.assertNotIn('mejor seed', src.lower())

    def test_veredicto_test_es_descriptivo(self):
        src = ''.join(celdas('04_redes_neuronales_paso4_3.ipynb')[38]['source'])
        self.assertFalse(any(isinstance(n, ast.If) for n in ast.walk(ast.parse(src))))
        for afirmacion in ('significancia', 'fuera del ruido', 'robusta', 'MEJORA', 'EMPEORA'):
            self.assertNotIn(afirmacion, src)
        self.assertIn('descriptiv', src.lower())

    def test_comparacion_no_se_hace_pasar_por_replica(self):
        src = codigo('04_redes_neuronales_paso4_4_B.ipynb')
        self.assertNotIn('ganadores del estudio de sensibilidad del 4.3', ''.join(''.join(c['source']) for c in celdas('04_redes_neuronales_paso4_4_B.ipynb') if c['cell_type'] == 'markdown'))
        self.assertIn('comparación histórica independiente', ''.join(''.join(c['source']) for c in celdas('04_redes_neuronales_paso4_4_B.ipynb') if c['cell_type'] == 'markdown'))
        self.assertNotIn("'LSTM Tuneada (Paso 4.3)'", src)


if __name__ == '__main__':
    unittest.main()
