# Etapa 2 — Limpieza y Transformación de Datos

> De datos crudos a datasets listos para modelar.

---

## 🎯 Objetivo

Tomar las fuentes originales (Excels y CSVs heterogéneos de Secretaría de Energía, CAMMESA, World Bank, Our World in Data) y producir cuatro datasets limpios, consistentes y listos para alimentar las etapas de modelado:

| Dataset producido | Filas | Cobertura | Uso aguas abajo |
|---|---|---|---|
| `dataset_global.csv` | 464 | 16 países seleccionados, 1990–2018 | Etapa 3 (regresión) y Etapa 4.1 (MLP) |
| `dataset_argentina_anual.csv` | 30 | 1992–2021 | Análisis nacional histórico |
| `dataset_argentina_mensual.csv` | 96 | 2017–2024 (mensual) | Etapa 4.2 y 4.3 (LSTM) |
| `dataset_argentina_provincias.csv` | 218 | Provincias × año × fuente | Análisis subnacional |

---

## 📓 Notebook

- [`02_limpieza_transformacion.ipynb`](./02_limpieza_transformacion.ipynb)

---

## 🔧 Decisiones de limpieza relevantes

- **Selección de países:** del dataset crudo de Our World in Data (que incluye ~200 entidades, varias de ellas agregaciones como "World", "OECD members", "High income"), se seleccionaron 16 países representativos para el análisis. La selección combina grandes emisores, economías latinoamericanas y productores de energía, garantizando variabilidad en perfiles energéticos.
- **Cálculo de variables derivadas:** `co2_per_capita`, `pbi_per_capita`, `co2_per_pbi`, `co2_per_energy` se computan a partir de las variables base, eliminando filas donde el denominador es nulo.
- **Unificación de unidades:** energía siempre en GWh para Argentina y Mtoe/TWh para datos globales (manteniendo la convención de la fuente).
- **Tratamiento de faltantes:** se eliminaron filas con datos críticos faltantes en lugar de imputarlos, para no introducir sesgo en el modelado.
- **Argentina anual vs mensual:** se mantuvieron como datasets separados porque cubren diferentes ventanas temporales y granularidades — mezclarlos artificialmente perdería información.

---

## 📂 Archivos en esta carpeta

| Archivo | Descripción |
|---|---|
| `02_limpieza_transformacion.ipynb` | Notebook con todo el pipeline de limpieza |
| `README.md` | Este archivo |

> Los **datasets de salida** están en [`../datos/limpios/`](../datos/limpios/).

---

## ➡️ Siguiente etapa

[**`03_Modelado_ML/`**](../03_Modelado_ML/) — modelos clásicos de machine learning sobre los datasets limpios.
