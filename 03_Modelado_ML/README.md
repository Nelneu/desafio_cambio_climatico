# Etapa 3 — Modelado con Machine Learning Clásico

> Antes de las redes neuronales, los modelos clásicos. Línea de base sólida.

---

## 🎯 Objetivo

Aplicar técnicas clásicas de machine learning para responder preguntas concretas sobre los datos:

- **Regresión:** ¿se puede predecir el CO₂ per cápita de un país a partir de variables socioeconómicas y energéticas? *(supervisado, target continuo)*
- **Series temporales:** ¿se puede pronosticar la generación renovable mensual de Argentina con métodos clásicos como ARIMA?
- **Clustering:** ¿agrupan los países en perfiles energéticos coherentes mediante K-Means? *(no supervisado)*

Los resultados de esta etapa funcionan como **líneas de base** para comparar con la Etapa 4 (redes neuronales); no se presupone que las redes las superen.

---

## 📓 Notebook

- [`03_modelado_ml.ipynb`](./03_modelado_ml.ipynb) — o su [HTML](./03_modelado_ml.html), instantánea anterior no regenerada con este cambio de rutas

---

## 📍 Rutas y dependencia

Ejecutar primero la Etapa 2: este notebook lee cuatro CSV de `datos/limpios/` y escribe `datos/intermedios/resultados_modelos_etapa3.csv` (crea el directorio solo al exportar). El paso 4.1 lee exactamente ese resultado junto con los CSV limpios y escribe `datos/intermedios/resultados_paso_4_1_mlp_regresion.csv`. Desde la raíz o esta carpeta, la raíz se encuentra por `README.md` y `datos/` en el directorio de trabajo o sus ancestros. Desde fuera, montar Drive en Colab si corresponde y definir `os.environ['CLIMATE_PROJECT_ROOT']` apuntando a la raíz antes de ejecutar las celdas; el override se valida. Si falta un CSV, se informa su ruta y no se busca uno alternativo. Los HTML existentes son instantáneas, no resultados recalculados. La regresión tabular ahora ajusta el escalador solo en train y dentro de cada fold de CV; los números históricos de esta página y las salidas previas no son métricas recalculadas con ese protocolo. El split aleatorio por fila conserva países y años compartidos entre conjuntos: no mide generalización a países o años no vistos.

## 🧪 Modelos entrenados

| Tipo | Modelo | Dataset | Métrica clave |
|---|---|---|---|
| Regresión lineal múltiple | OLS | `dataset_global.csv` | R² ≈ 0.73 |
| Regresión regularizada | Ridge, Lasso | `dataset_global.csv` | R² ≈ 0.73 |
| Regresión lineal con variables derivadas | OLS + ingeniería de variables | `dataset_global.csv` | R² ≈ 0.967 en la ejecución aislada de DR-1 |
| Series temporales | ARIMA | `dataset_argentina_mensual.csv` | RMSE sobre validación |
| Clustering | K-Means + PCA | `dataset_global.csv` | Silhouette + interpretación |

---

## 🔍 Principales hallazgos

- **Con las variables originales**, OLS, Ridge y Lasso rondan R² ≈ 0.73; la regularización no mejora sustancialmente ese resultado. **Con variables derivadas**, una regresión lineal alcanzó R² ≈ 0.967 en una ejecución aislada: 0.73 no es un techo demostrado de la familia lineal. El split aleatorio por fila y la selección de variables limitan la interpretación de esas cifras.
- **ARIMA captura la tendencia y la estacionalidad anual** de la generación renovable mensual, pero subestima los picos.
- **K-Means agrupa los países en perfiles energéticos interpretables**: economías intensivas en carbón, economías basadas en hidro, economías con alta penetración eólica/solar, etc.

> 💡 **Pregunta para la Etapa 4:** comparar redes neuronales con baselines lineales tanto de variables originales como derivadas, usando la misma partición y sin afirmar superioridad antes de medirla. Ver [`../04_Redes_Neuronales/`](../04_Redes_Neuronales/).

---

## 📂 Archivos en esta carpeta

| Archivo | Descripción |
|---|---|
| `03_modelado_ml.ipynb` | Notebook con todos los modelos clásicos |
| `03_modelado_ml.html` | Versión renderizada del notebook, con todas las salidas y gráficos |
| `README.md` | Este archivo |

---

## ➡️ Siguiente etapa

[**`04_Redes_Neuronales/`**](../04_Redes_Neuronales/) — MLP para regresión, LSTM para series temporales, y comparación final.
