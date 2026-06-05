# Cambio Climático y Energías Renovables en Argentina

Análisis de datos y modelado predictivo sobre la transición energética argentina, con foco en la relación entre emisiones de CO₂, generación renovable y variables socioeconómicas.

> **Desafío Profesional — Certificación en Data Science**
> Digital House · 2025
> Autor: Nelson Pullella ([@Nelneu](https://github.com/Nelneu))

---

## 🎯 Objetivos del proyecto

Este desafío recorre las cuatro etapas clásicas de un proyecto de ciencia de datos aplicadas a un dominio real: **el cambio climático y la matriz energética argentina**. La pregunta central que articula todo el trabajo es:

> *¿Qué factores explican las emisiones de CO₂ de un país, y cómo está evolucionando Argentina en su transición hacia energías renovables?*

Para responderla, el proyecto integra datos globales (16 países seleccionados, 1990–2018) y datos específicos de Argentina (anuales, mensuales y por provincia), y aplica desde modelos lineales clásicos hasta redes neuronales profundas (MLP y LSTM).

---

## 📁 Estructura del repositorio

```
desafio_cambio_climatico/
├── 01_EDA/                       Análisis exploratorio de los datos
├── 02_Limpieza/                  Limpieza y transformación de datasets
├── 03_Modelado_ML/               Machine learning clásico (Ridge, Lasso, ARIMA, K-Means)
├── 04_Redes_Neuronales/          Deep learning (MLP, LSTM, comparación ML vs DL)
├── 05_Storytelling/              Capstone narrativo: el informe final del proyecto
├── datos/
│   ├── originales/               Fuentes públicas (instrucciones de descarga)
│   └── limpios/                  Datasets procesados, listos para usar
├── reportes/                     HTMLs renderizados de los notebooks
└── docs/                         Plan de trabajo y documentación
```

Cada carpeta numerada corresponde a una etapa del proyecto y contiene su propio `README.md` con el contexto, los hallazgos y los archivos relevantes.

---

## 🚀 Cómo ejecutar los notebooks

Los notebooks están preparados para ejecutarse **tanto en Google Colab como localmente**, sin modificación. Detectan el entorno automáticamente.

### Opción 1 — Local (recomendada para evaluación)

```bash
# 1. Clonar el repositorio
git clone https://github.com/Nelneu/desafio_cambio_climatico.git
cd desafio_cambio_climatico

# 2. Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate           # Linux/Mac
# venv\Scripts\activate            # Windows
pip install -r requirements.txt

# 3. Abrir Jupyter
jupyter notebook
```

### Opción 2 — Google Colab

Subir la carpeta `datos/limpios/` a tu Drive en `MyDrive/desafio_profesional/datos_limpios/` y abrir cualquier notebook desde Colab. La primera celda monta el Drive automáticamente.

---

## 🗺️ Recorrido sugerido

Para una lectura ordenada del proyecto, recomiendo seguir las etapas en orden:

| Etapa | Carpeta | Contenido |
|---|---|---|
| 1 | [`01_EDA/`](./01_EDA/) | Exploración visual, distribuciones, correlaciones |
| 2 | [`02_Limpieza/`](./02_Limpieza/) | Limpieza, integración de fuentes, datasets finales |
| 3 | [`03_Modelado_ML/`](./03_Modelado_ML/) | Regresión lineal, regularización, clustering, ARIMA |
| 4 | [`04_Redes_Neuronales/`](./04_Redes_Neuronales/) | MLP global, LSTM Argentina, comparación ML vs DL |
| 5 | [`05_Storytelling/`](./05_Storytelling/) | Capstone narrativo: las 4 preguntas centrales y sus respuestas |

Si querés ir directo al **cierre del proyecto**, abrí la [Etapa 5 — Informe Final](./05_Storytelling/) o su [versión renderizada en HTML](./05_Storytelling/05_informe_final.html). Está pensado para leerse de corrido, sin necesidad de ejecutar código.

---

## 🔍 Hallazgos destacados

- **Las MLPs aprenden ratios implícitos.** En el modelado de CO₂ per cápita, la red neuronal alcanzó R² ≈ 0.97 frente a R² ≈ 0.73 de los modelos lineales. La diferencia se explica porque la MLP aprende internamente la variable derivada `energía_per_cápita = energía_Mtoe / población`, que correlaciona con el target a ρ = 0.99. Verificado empíricamente: al sumar la variable derivada al pipeline, Ridge iguala el desempeño de la MLP.

- **Las renovables "computables" subestiman la matriz limpia.** La Ley 27.191 solo contabiliza hidroeléctricas pequeñas (≤50 MW), por lo que represas como El Chocón quedan fuera del ratio renovable oficial. Para evaluar la matriz energética completa hay que distinguir explícitamente entre "renovables Ley 27.191" y "fuentes limpias totales" — un matiz importante a la hora de comparar Argentina con otros países.

- **El LSTM captura estacionalidad mensual.** El modelo de series temporales sobre la generación renovable mensual de Argentina detecta los patrones estacionales propios de cada fuente (vientos patagónicos en invierno, radiación solar en verano), lo que lo vuelve útil para forecasting energético operativo.

---

## 📊 Datos utilizados

| Dataset | Fuente principal | Uso |
|---|---|---|
| `dataset_global.csv` | Our World in Data (CO₂ Data) | Modelado supervisado (Etapa 3 y 4.1) |
| `dataset_argentina_anual.csv` | Secretaría de Energía + INDEC | Análisis nacional histórico |
| `dataset_argentina_mensual.csv` | CAMMESA | Series temporales (Etapa 4.2 y 4.3) |
| `dataset_argentina_provincias.csv` | Secretaría de Energía | Análisis subnacional |

Las fuentes originales y el procedimiento para descargarlas están documentados en [`datos/originales/README.md`](./datos/originales/README.md).

---

## 🛠️ Stack técnico

- **Lenguaje:** Python 3.10+
- **Análisis y modelado:** pandas, numpy, scikit-learn, statsmodels
- **Deep learning:** TensorFlow / Keras
- **Visualización:** matplotlib, seaborn
- **Entorno:** Jupyter, Google Colab

Lista completa en [`requirements.txt`](./requirements.txt).

---

## 📝 Licencia y contacto

Proyecto académico desarrollado en el marco de la Certificación en Data Science de Digital House.

Datos públicos de Secretaría de Energía de la Nación, CAMMESA, INDEC y Our World in Data — utilizados con fines educativos.
