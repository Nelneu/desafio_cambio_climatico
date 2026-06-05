# Etapa 4 — Redes Neuronales (Deep Learning)

> Donde las redes superan a los lineales — y descubrimos por qué.

---

## 🎯 Objetivo

Aplicar redes neuronales modernas a los dos problemas centrales del proyecto:

1. **Regresión global de CO₂ per cápita** — ¿puede una MLP superar el techo de R² ≈ 0.73 que dejaron los modelos lineales en la Etapa 3?
2. **Forecasting de generación renovable mensual** — ¿puede una LSTM mejorar el ARIMA en Argentina?

Y, fundamentalmente: **entender por qué** cuando la red gana, y **comparar rigurosamente** ambos enfoques.

---

## 📓 Notebooks

| Paso | Notebook | Tema |
|---|---|---|
| 4.1 | `04_1_mlp_regresion.ipynb` | MLP para regresión global de CO₂ per cápita |
| 4.2 | `04_2_lstm_series_temporales.ipynb` | LSTM sobre serie mensual de Argentina |
| 4.3 | `04_3_lstm_fine_tuning.ipynb` | Optimización del LSTM (hiperparámetros, regularización) |
| 4.4.A | `04_4_A_comparacion_regresion.ipynb` | Comparación ML vs DL — bloque de regresión |
| 4.4.B | `04_4_B_comparacion_forecasting.ipynb` | Comparación ML vs DL — bloque de series temporales |
| 4.4.C | `04_4_C_sintesis_transversal.ipynb` | Síntesis transversal y guía decisional |

> 💡 **¿Por qué 4.4 está dividido en tres notebooks?** La comparación ML vs Deep Learning aborda dos familias de problemas (regresión y forecasting) con métodos y datasets distintos. Cada uno merece su propio análisis aislado (4.4.A y 4.4.B), y la síntesis cruzada (4.4.C) requiere combinar resultados de ambos. Mantenerlos separados hace cada notebook más legible y evita un único archivo monstruoso.

---

## 🏆 Hallazgos clave

### Paso 4.1 — Las MLPs aprenden ratios implícitos

- Tres arquitecturas MLP probadas, todas con **R² ≈ 0.97** en validación, frente al **R² ≈ 0.73** de Ridge/Lasso/regresión múltiple.
- Diagnósticos de overfitting descartados (loss train ≈ loss val, métricas estables en CV).
- **Hipótesis verificada empíricamente:** la MLP aprende internamente la variable derivada `energía_per_cápita = energía_Mtoe / población`, que correlaciona con `co2_per_capita` a ρ = 0.99.
- **Prueba contundente:** al sumar la variable derivada a Ridge, el modelo lineal **iguala** el desempeño de la MLP. La red no tenía "más capacidad" en sentido genérico — tenía la capacidad específica de componer un cociente vía ReLU, que el modelo lineal por construcción no puede aprender.

> Este hallazgo es **el insight técnico central del proyecto**: la superioridad del deep learning no es magia, es composición no lineal — y se puede inspeccionar y reproducir en un modelo lineal una vez que se entiende.

### Paso 4.2 — LSTM sobre series mensuales

- Modelo entrenado sobre `dataset_argentina_mensual.csv` (96 meses).
- Ventaneo temporal con secuencias de longitud configurable.
- Captura estacionalidad y tendencia, mejor que ARIMA en validación.

### Paso 4.3 — Fine-tuning del LSTM

- Búsqueda manual de hiperparámetros (capas, neuronas, dropout, longitud de ventana, learning rate).
- Análisis de curvas de loss para ajustar regularización y early stopping.
- Modelo final más estable, con mejor generalización.

### Paso 4.4 — Comparación rigurosa ML vs DL

- **Bloque A (regresión):** comparación cabeza a cabeza de Ridge, Lasso y MLP (con 3 seeds para robustez) sobre el dataset global. Tabla A consolidada con métricas y costos computacionales.
- **Bloque B (forecasting):** comparación de ARIMA, LSTM Simple y LSTM Tuneada sobre la serie mensual argentina. Tabla B con visualizaciones de predicciones.
- **Bloque C (síntesis):** tabla transversal con 7 modelos × 6 dimensiones (precisión, costo computacional, interpretabilidad, datos requeridos, hiperparámetros, complejidad). Cierra con una **guía decisional** sobre cuándo conviene cada enfoque — un aporte práctico que va más allá del proyecto.

---

## 📂 Archivos en esta carpeta

| Archivo | Descripción |
|---|---|
| `04_1_mlp_regresion.ipynb` | MLP para regresión global |
| `04_2_lstm_series_temporales.ipynb` | LSTM sobre serie mensual |
| `04_3_lstm_fine_tuning.ipynb` | Optimización del LSTM |
| `04_4_A_comparacion_regresion.ipynb` | Comparación ML vs DL — regresión |
| `04_4_B_comparacion_forecasting.ipynb` | Comparación ML vs DL — forecasting |
| `04_4_C_sintesis_transversal.ipynb` | Síntesis transversal |
| `README.md` | Este archivo |

> Las versiones renderizadas en HTML de estos notebooks están en [`../reportes/`](../reportes/) — útiles para revisar resultados sin ejecutar el código.

---

## ➡️ Siguiente etapa

[**`05_Storytelling/`**](../05_Storytelling/) — el capstone narrativo del proyecto, donde los hallazgos técnicos se traducen en respuestas y recomendaciones para un lector no especialista.

## 🔙 Etapa anterior

[**`03_Modelado_ML/`**](../03_Modelado_ML/) — los modelos clásicos cuyos resultados las redes neuronales buscan superar.
