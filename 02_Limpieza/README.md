# Etapa 2 — Limpieza y Transformación de Datos

> De datos crudos a datasets listos para modelar.

---

## 🎯 Objetivo

El ETL espera cinco libros Excel (DS1–DS5) en `datos/originales/` y exporta cinco CSV limpios para las etapas siguientes. Sus nombres exactos y hojas se detallan en el [inventario de entradas](../datos/originales/README.md); la procedencia institucional de esos libros no está verificada. El ETL no lee un CSV de Our World in Data.

| Dataset producido | Filas | Cobertura | Uso aguas abajo |
|---|---|---|---|
| `dataset_global.csv` | 464 | 16 países seleccionados, 1990–2018 | Etapa 3 (regresión) y Etapa 4.1 (MLP) |
| `dataset_argentina_anual.csv` | 30 | Argentina × año, 1990–2019 | Análisis nacional histórico |
| `dataset_argentina_mensual.csv` | 96 | Argentina × mes, 96 meses consecutivos, 2011-01–2018-12 | Etapa 4.2 y 4.3 (LSTM) |
| `dataset_argentina_provincias.csv` | 218 | Provincia × región × año × fuente, 2011–2018 (long) | Análisis subnacional |
| `dataset_argentina_provincias_wide.csv` | 107 | Provincia × año, 2011–2018 (wide) | Etapa 3 (clustering) |

> **Alcance de la tabla:** conteos y coberturas observados en los cinco CSV versionados de `datos/limpios/`, no cobertura ni procedencia verificadas de los libros Excel de entrada. Son una instantánea existente, no una garantía de las filas que produciría una ejecución futura del ETL.
>
> **Campos vacíos observados:** con `csv.DictReader` (cadena vacía), el CSV global contiene 18 celdas vacías y el anual 231 celdas vacías; el mensual y el provincial long no contienen celdas vacías. Estos conteos no prueban que se hayan eliminado filas por faltantes.

---

## 📓 Notebook

- [`02_limpieza_transformacion.ipynb`](./02_limpieza_transformacion.ipynb) — o su [HTML](./02_limpieza_transformacion.html), instantánea anterior que no se regeneró con este cambio de rutas

---

## 📍 Rutas y ejecución

Colocar los cinco libros con nombres exactos en `../datos/originales/` (véase su [inventario](../datos/originales/README.md)). Desde la raíz del proyecto o esta carpeta, el notebook detecta el primer ancestro con `README.md` y `datos/`; desde fuera (por ejemplo Colab), montar Drive y configurar `os.environ['CLIMATE_PROJECT_ROOT']` con la ruta de la **raíz del proyecto** antes de ejecutar la carga. Una raíz inválida o un libro ausente produce error explícito; no se elige otro dataset. La exportación crea `datos/limpios/` si hace falta y escribe allí cinco CSV (incluido `dataset_argentina_provincias_wide.csv`). Luego ejecutar la Etapa 3; no se regeneraron los HTML.

## 🔧 Decisiones de limpieza relevantes

- **Selección de países:** el ETL construye el dataset global a partir de DS2 (estadísticas de energía mundial), DS3 (PBI per cápita) y DS4 (población), filtra agregaciones y selecciona países para el análisis. No consume el CSV de Our World in Data; los editores de DS2–DS4 siguen sin verificar.
- **Cálculo de variables derivadas:** `co2_per_capita`, `pbi_per_capita`, `co2_per_pbi`, `co2_per_energy` se calculan a partir de variables base. No se puede afirmar que los denominadores nulos hayan provocado la eliminación de filas; el CSV global conserva campos vacíos.
- **Unificación de unidades:** energía siempre en GWh para Argentina y Mtoe/TWh para datos globales (manteniendo la convención de la fuente).
- **Tratamiento de faltantes:** los CSV global y anual conservan campos vacíos; no hay evidencia aquí de una eliminación general de filas con datos críticos faltantes.
- **Argentina anual vs mensual:** se mantuvieron como datasets separados porque cubren diferentes ventanas temporales y granularidades — mezclarlos artificialmente perdería información.

---

## 📂 Archivos en esta carpeta

| Archivo | Descripción |
|---|---|
| `02_limpieza_transformacion.ipynb` | Notebook con todo el pipeline de limpieza |
| `02_limpieza_transformacion.html` | Versión renderizada del notebook, con todas las salidas |
| `README.md` | Este archivo |

> Los **datasets de salida** están en [`../datos/limpios/`](../datos/limpios/).

---

## ➡️ Siguiente etapa

[**`03_Modelado_ML/`**](../03_Modelado_ML/) — modelos clásicos de machine learning sobre los datasets limpios.
