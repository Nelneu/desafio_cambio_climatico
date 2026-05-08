# Etapa 3 — Modelado con Machine Learning Clásico

> Antes de las redes neuronales, los modelos clásicos. Línea de base sólida.

---

## 🎯 Objetivo

Aplicar técnicas clásicas de machine learning para responder preguntas concretas sobre los datos:

- **Regresión:** ¿se puede predecir el CO₂ per cápita de un país a partir de variables socioeconómicas y energéticas? *(supervisado, target continuo)*
- **Series temporales:** ¿se puede pronosticar la generación renovable mensual de Argentina con métodos clásicos como ARIMA?
- **Clustering:** ¿agrupan los países en perfiles energéticos coherentes mediante K-Means? *(no supervisado)*

Los resultados de esta etapa funcionan como **línea de base** que la Etapa 4 (redes neuronales) buscará superar.

---

## 📓 Notebook

- [`03_modelos_ml.ipynb`](./03_modelos_ml.ipynb)

---

## 🧪 Modelos entrenados

| Tipo | Modelo | Dataset | Métrica clave |
|---|---|---|---|
| Regresión lineal múltiple | OLS | `dataset_global.csv` | R² ≈ 0.73 |
| Regresión regularizada | Ridge, Lasso | `dataset_global.csv` | R² ≈ 0.73 |
| Series temporales | ARIMA | `dataset_argentina_mensual.csv` | RMSE sobre validación |
| Clustering | K-Means + PCA | `dataset_global.csv` | Silhouette + interpretación |

---

## 🔍 Principales hallazgos

- **Las regresiones lineales/regularizadas se topan con un techo en R² ≈ 0.73** sobre el dataset global. La regularización (Ridge/Lasso) no mejora sustancialmente el desempeño, lo que sugiere que el problema no es overfitting sino **un límite de la familia lineal**.
- **ARIMA captura la tendencia y la estacionalidad anual** de la generación renovable mensual, pero subestima los picos.
- **K-Means agrupa los países en perfiles energéticos interpretables**: economías intensivas en carbón, economías basadas en hidro, economías con alta penetración eólica/solar, etc.

> 💡 **Hipótesis abierta para la Etapa 4:** el techo lineal sugiere que existen relaciones no lineales (¿ratios? ¿interacciones?) que un modelo más flexible podría capturar. Esta hipótesis se verifica en [`../04_Redes_Neuronales/`](../04_Redes_Neuronales/).

---

## 📂 Archivos en esta carpeta

| Archivo | Descripción |
|---|---|
| `03_modelos_ml.ipynb` | Notebook con todos los modelos clásicos |
| `README.md` | Este archivo |

---

## ➡️ Siguiente etapa

[**`04_Redes_Neuronales/`**](../04_Redes_Neuronales/) — MLP para regresión, LSTM para series temporales, y comparación final.
