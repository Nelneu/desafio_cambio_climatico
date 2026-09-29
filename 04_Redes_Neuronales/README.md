# Etapa 4 — Redes Neuronales (Deep Learning)

> Comparaciones descriptivas de redes y baselines, con protocolos y límites explícitos.

---

## 🎯 Objetivo

Aplicar redes neuronales modernas a los dos problemas centrales del proyecto:

1. **Regresión global de CO₂ per cápita** — ¿cómo se compara una MLP con Ridge bajo cada protocolo tabular?
2. **Forecasting de generación renovable mensual** — ¿puede una LSTM mejorar el ARIMA en Argentina?

Y comparar sus métricas observadas sin atribuir mecanismos internos, significancia ni ventajas de despliegue a partir de estos splits.

---

## 📓 Notebooks

| Paso | Notebook | Ver sin ejecutar | Tema |
|---|---|---|---|
| 4.1 | [`04_redes_neuronales_paso4_1.ipynb`](./04_redes_neuronales_paso4_1.ipynb) | [HTML](./04_redes_neuronales_paso4_1.html) | MLP para regresión global de CO₂ per cápita |
| 4.2 | [`04_redes_neuronales_paso4_2.ipynb`](./04_redes_neuronales_paso4_2.ipynb) | [HTML](./04_redes_neuronales_paso4_2.html) | LSTM sobre serie mensual de Argentina |
| 4.3 | [`04_redes_neuronales_paso4_3.ipynb`](./04_redes_neuronales_paso4_3.ipynb) | [HTML](./04_redes_neuronales_paso4_3.html) | Optimización del LSTM (hiperparámetros, regularización) |
| 4.4.A | [`04_redes_neuronales_paso4_4_A.ipynb`](./04_redes_neuronales_paso4_4_A.ipynb) | [HTML](./04_redes_neuronales_paso4_4_A.html) | Comparación ML vs DL — bloque de regresión |
| 4.4.B | [`04_redes_neuronales_paso4_4_B.ipynb`](./04_redes_neuronales_paso4_4_B.ipynb) | [HTML](./04_redes_neuronales_paso4_4_B.html) | Comparación ML vs DL — bloque de series temporales |
| 4.4.C | [`04_redes_neuronales_paso4_4_C.ipynb`](./04_redes_neuronales_paso4_4_C.ipynb) | [HTML](./04_redes_neuronales_paso4_4_C.html) | Síntesis transversal y guía decisional |

> 💡 **¿Por qué 4.4 está dividido en tres notebooks?** La comparación ML vs Deep Learning aborda dos familias de problemas (regresión y forecasting) con métodos y datasets distintos. Cada uno merece su propio análisis aislado (4.4.A y 4.4.B), y la síntesis cruzada (4.4.C) requiere combinar resultados de ambos. Mantenerlos separados hace cada notebook más legible y evita un único archivo monstruoso.

---

## 🏆 Hallazgos clave

### Paso 4.1 — Regresión tabular y variable derivada

- En 4.1, MLP Medio registró **R² 0.9796** y Ridge **0.7349**. En 4.4.A, otro holdout aleatorio por filas registró MLP Medio **0.9264 ± 0.0103** (3 seeds) y Ridge **0.7568**. No son una sola medición ni prueban generalización fuera de los países/años observados.
- Las curvas de loss y las métricas guardadas permiten inspeccionar el ajuste en esos splits; no descartan sobreajuste ni prueban generalización.
- El análisis histórico examinó la variable derivada `energía_per_cápita = energía_Mtoe / población` y su correlación reportada con `co2_per_capita` (ρ = 0.99). Esa asociación no demuestra que la MLP construya el cociente internamente.
- En la comparación histórica con esa variable calculada manualmente, Ridge alcanzó una métrica cercana a la MLP en la partición examinada. No se evaluó el mecanismo interno de la red ni su comportamiento fuera de esa partición.

> Estos resultados motivan comparar ingeniería manual de variables y MLP en cada protocolo; no identifican una causa de las diferencias de R² ni una superioridad general.

### Paso 4.2 — LSTM sobre series mensuales

- Modelo entrenado sobre `dataset_argentina_mensual.csv` (96 meses).
- Ventaneo temporal con secuencias de longitud configurable.
- La comparación en la partición de validación es descriptiva; no se demostró que la red haya aprendido patrones estacionales específicos ni que generalice mejor que ARIMA.

### Paso 4.3 — Fine-tuning del LSTM

- Búsqueda manual de hiperparámetros (capas, neuronas, dropout, longitud de ventana, learning rate).
- Análisis de curvas de loss para ajustar regularización y early stopping.
- En la ejecución aislada DR-3, validación recursiva 2017 (train 2011–2016) seleccionó bs=32, lr=5e-4, sin regularización; reentrenamiento pre-2018 y test 2018: MAPE **20.43 ± 0.10%**, MAE **72.75 ± 0.34 GWh**, RMSE **107.93 ± 0.27 GWh** (3 seeds). En esa ejecución simple 20.74% y ARIMA 26.68% MAPE.

### Paso 4.4 — Comparación rigurosa ML vs DL

- **Bloque A (regresión):** comparación cabeza a cabeza de Ridge, Lasso y MLP (con 3 seeds para robustez) sobre el dataset global. Tabla A consolidada con métricas y costos computacionales.
- **Bloque B (forecasting):** ejecución independiente de una alternativa fija histórica (bs=4, lr=5e-3), **no** reproduce 4.3: MAPE **20.70 ± 3.47%** (3 seeds); simple **20.61%** y ARIMA **26.68%**.
- **Bloque C (síntesis):** constantes fuente reconciliadas con 4.4.A y B; no incorpora el modelo seleccionado en 4.3 al ranking ni reentrena. Sus salidas y HTML siguen históricos.

---

## 📂 Archivos en esta carpeta

| Archivo | Descripción |
|---|---|
| `04_redes_neuronales_paso4_1.ipynb` + `.html` | MLP para regresión global |
| `04_redes_neuronales_paso4_2.ipynb` + `.html` | LSTM sobre serie mensual |
| `04_redes_neuronales_paso4_3.ipynb` + `.html` | Optimización del LSTM |
| `04_redes_neuronales_paso4_4_A.ipynb` + `.html` | Comparación ML vs DL — regresión |
| `04_redes_neuronales_paso4_4_B.ipynb` + `.html` | Comparación ML vs DL — forecasting |
| `04_redes_neuronales_paso4_4_C.ipynb` + `.html` | Síntesis transversal |
| `README.md` | Este archivo |

> 💡 Los HTML y salidas almacenadas son instantáneas históricas, no resultados recalculados con el ajuste del escalador solo en train en 4.1 y 4.4.A ni con el holdout temporal de 4.3. Las mediciones aisladas DR-3 y su protocolo están en [validación neuronal](../docs/neural-validation.md); los outputs de notebooks fuente y HTML siguen históricos, sin regenerar. Las diferencias observadas no prueban superioridad estadística ni una explicación causal. El split tabular aleatorio por fila comparte países y años entre train/test; no demuestra generalización a países o años nuevos.

---

## ➡️ Siguiente etapa

[**`05_Storytelling/`**](../05_Storytelling/) — el capstone narrativo del proyecto, donde los hallazgos técnicos se traducen en respuestas y recomendaciones para un lector no especialista.

## 🔙 Etapa anterior

[**`03_Modelado_ML/`**](../03_Modelado_ML/) — los modelos clásicos cuyos resultados las redes neuronales buscan superar.
