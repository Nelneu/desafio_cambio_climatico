"""Regression guards for tabular random-row preprocessing in source notebooks."""
import ast
import json
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = {
    "stage3": ("03_Modelado_ML/03_modelado_ml.ipynb", (8, 13)),
    "stage4_1": ("04_Redes_Neuronales/04_redes_neuronales_paso4_1.ipynb", (5, 23)),
    "stage4_4A": ("04_Redes_Neuronales/04_redes_neuronales_paso4_4_A.ipynb", (7,)),
}


def code(path, index):
    cell = json.loads((ROOT / path).read_text(encoding="utf-8"))["cells"][index]
    assert cell["cell_type"] == "code"
    return "".join(cell["source"])


def calls(tree, name):
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call) and
            isinstance(n.func, ast.Name) and n.func.id == name]


class TabularPreprocessingTests(unittest.TestCase):
    def test_scalers_fit_only_after_split(self):
        for label, (path, indices) in NOTEBOOKS.items():
            for index in indices:
                with self.subTest(notebook=label, cell=index):
                    tree = ast.parse(code(path, index))
                    split_lines = [n.lineno for n in calls(tree, "train_test_split")]
                    self.assertEqual(len(split_lines), 1)
                    fit_lines = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Call)
                                 and isinstance(n.func, ast.Attribute)
                                 and n.func.attr in ("fit", "fit_transform")
                                 and isinstance(n.func.value, ast.Name)
                                 and n.func.value.id.startswith("scaler")]
                    self.assertTrue(fit_lines, "training scaler fit missing")
                    self.assertTrue(all(line > split_lines[0] for line in fit_lines))
                    self.assertFalse(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                                         and n.func.attr == "fit_transform" and n.args and
                                         isinstance(n.args[0], ast.Name) and
                                         n.args[0].id in ("X", "X_fe", "X_ext")
                                         for n in ast.walk(tree)))
                    self.assertIn("transform(X_test", code(path, index))

    def test_cv_and_grid_search_fit_scaler_per_fold(self):
        path = NOTEBOOKS["stage3"][0]
        for index in (8, 13, 15):
            with self.subTest(cell=index):
                source = code(path, index)
                tree = ast.parse(source)
                for call in calls(tree, "cross_val_score"):
                    self.assertIsInstance(call.args[0], ast.Call)
                    self.assertIsInstance(call.args[0].func, ast.Name)
                    self.assertEqual(call.args[0].func.id, "Pipeline")
                    self.assertNotIn("scaled", ast.unparse(call.args[1]))
        source = code(path, 11)
        self.assertEqual(source.count("GridSearchCV(Pipeline("), 2)
        self.assertIn("regressor__alpha", source)
        self.assertIn("named_steps['regressor'].coef_", source)
        for prefix in ("ridge_gs", "lasso_gs"):
            self.assertIn(f"{prefix}.fit(X_train_raw, y_train)", source)
            self.assertIn(f"{prefix}.predict(X_test_raw)", source)
        self.assertNotIn("X_scaled", code(path, 8))
        self.assertNotIn("X_fe_scaled", code(path, 15))

    def test_synthetic_test_outlier_does_not_affect_train_scaler(self):
        """Execute only the stage-3 preprocessing prefix on a tiny deterministic dataset."""
        path = NOTEBOOKS["stage3"][0]
        source = code(path, 8).split("# Regresión lineal múltiple")[0]
        rows = 30
        df = pd.DataFrame({
            "anio": np.arange(rows) + 1990, "pais": ["P"] * rows,
            "co2_per_capita": np.arange(rows, dtype=float),
            "pbi_per_capita": np.arange(rows, dtype=float),
            "share_renewables": np.arange(rows, dtype=float) + 3,
            "energy_Mtoe": np.arange(rows, dtype=float) + 5,
            "poblacion": np.arange(rows, dtype=float) + 10,
        })
        # A single held-out extreme row must not enter fit; split membership is unchanged.
        _, held_out, _, _ = train_test_split(df.index, df.index, test_size=0.2, random_state=42)
        df.loc[held_out[0], "pbi_per_capita"] = 1e9
        env = {"df_global": df, "StandardScaler": StandardScaler,
               "train_test_split": train_test_split}
        exec(compile(source, path, "exec"), env)
        raw_train, raw_test, _, _ = train_test_split(
            df[env["features"]], df["co2_per_capita"], test_size=0.2, random_state=42)
        np.testing.assert_allclose(env["scaler"].mean_, raw_train.mean().to_numpy())
        np.testing.assert_allclose(env["X_train"], env["scaler"].transform(raw_train))
        np.testing.assert_allclose(env["X_test"], env["scaler"].transform(raw_test))


if __name__ == "__main__":
    unittest.main()
