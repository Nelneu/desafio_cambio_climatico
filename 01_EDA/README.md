# Etapa 1 — Análisis Exploratorio de Datos (EDA)

> Primer contacto con los datos. Antes de modelar, entender.

---

## 🎯 Objetivo

Explorar las cuatro fuentes de datos del proyecto (global, Argentina anual, Argentina mensual y por provincia) para responder preguntas básicas:

- ¿Qué variables tenemos y de qué tipo son?
- ¿Cuántos países y años cubre cada dataset?
- ¿Hay valores faltantes? ¿Outliers? ¿Inconsistencias?
- ¿Qué relaciones se intuyen entre variables a simple vista?

Esta etapa **no toma decisiones de modelado**. Solo levanta hallazgos y abre interrogantes que las etapas siguientes van a responder.

---

## 📓 Notebook

- [`01_exploracion_visual.ipynb`](./01_exploracion_visual.ipynb)

---

## 🔍 Principales hallazgos

- El **dataset global** cubre 16 países seleccionados entre 1990 y 2018, con buena densidad de datos en variables socioeconómicas y energéticas. La selección incluye grandes emisores (China, EE.UU., India, Rusia), economías latinoamericanas (Argentina, Chile, Colombia) y productores de energía (Iran, Kuwait, Nigeria), entre otros.
- En Argentina, las **renovables explotan a partir de 2018** (Ley 27.191 + RenovAr), aunque desde una base baja.
- Hay **fuerte estacionalidad mensual** en la generación eólica y solar de Argentina, visible al desagregar por mes.
- El **CO₂ per cápita** se correlaciona muy fuerte con el **consumo energético per cápita** (ρ ≈ 0.99 en el dataset global).

---

## 📂 Archivos en esta carpeta

| Archivo | Descripción |
|---|---|
| `01_exploracion_visual.ipynb` | Notebook con todo el EDA: distribuciones, correlaciones, series temporales preliminares |
| `README.md` | Este archivo |

---

## ➡️ Siguiente etapa

[**`02_Limpieza/`**](../02_Limpieza/) — limpieza, transformación e integración de las fuentes en los datasets finales.
