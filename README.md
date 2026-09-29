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
│   ├── limpios/                  Datasets procesados, listos para usar
│   └── intermedios/              Resultados de modelado (se crea al exportar)
└── docs/                         Plan de trabajo y documentación
```

Cada carpeta numerada corresponde a una etapa del proyecto y contiene su propio `README.md` con el contexto, los hallazgos y los archivos relevantes. Los archivos `.html` existentes son **instantáneas de ejecuciones anteriores**: no se regeneraron al modificar las rutas y pueden mostrar rutas o resultados desactualizados.

---

## 🚀 Cómo ejecutar los notebooks

Los notebooks de las etapas 1–5 que leen datos (excepto 4.4C) resuelven la raíz buscando desde el directorio de trabajo actual hacia sus ancestros el primero que contenga `README.md` y `datos/`. Funciona desde la raíz o desde una carpeta de etapa; no depende de la ubicación del archivo `.ipynb`. Si se inicia fuera del árbol, definir `CLIMATE_PROJECT_ROOT` con la ruta **de la raíz**: tiene prioridad y se valida (sin recurrir silenciosamente a otra carpeta). Las entradas faltantes producen un error con la ruta esperada; no se descargan ni se sustituyen datos.

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

# 3. Colocar los cinco Excel con los nombres exactos en datos/originales/
#    (ver datos/originales/README.md); luego abrir Jupyter
jupyter notebook
```

La lectura de los Excel originales mediante `pandas.read_excel` requiere motores separados: `openpyxl` para archivos `.xlsx` y `xlrd` para archivos `.xls`. Ambos figuran como dependencias directas en `requirements.txt`; la instalación y la ejecución de los notebooks no se verificaron aquí.

### Opción 2 — Google Colab

Montar Drive **manualmente** en una celda de Colab, mantener una copia del proyecto con `README.md` y `datos/` juntos y configurar la raíz **antes** de ejecutar las celdas de lectura:

```python
from google.colab import drive
drive.mount('/content/drive')
import os
os.environ['CLIMATE_PROJECT_ROOT'] = '/content/drive/MyDrive/desafio_cambio_climatico'
```

Ajustar el valor al lugar real de la carpeta completa; no apuntar a `datos/` ni a un CSV. Para ejecutar la limpieza hacen falta los cinco libros en `datos/originales/`. Si el directorio de trabajo está dentro del proyecto y no se usa override, no se requiere configurar la variable.

---

## 🗺️ Recorrido sugerido

Para ejecutar desde las fuentes: 01 (exploración opcional) → 02 (requiere los cinco libros originales; escribe cinco CSV en `datos/limpios/`) → 03 (lee CSV limpios y escribe `datos/intermedios/resultados_modelos_etapa3.csv`) → 4.1 (lee ese resultado y escribe `datos/intermedios/resultados_paso_4_1_mlp_regresion.csv`). Los pasos 4.2, 4.3, 4.4A, 4.4B y 05 leen los CSV limpios según corresponda; 4.4C queda fuera de este contrato. Las carpetas de salida se crean solo al exportar. Para una lectura ordenada del proyecto, recomiendo seguir las etapas en orden:

| Etapa | Carpeta | Contenido |
|---|---|---|
| 1 | [`01_EDA/`](./01_EDA/) | Exploración visual, distribuciones, correlaciones |
| 2 | [`02_Limpieza/`](./02_Limpieza/) | Limpieza, integración de fuentes, datasets finales |
| 3 | [`03_Modelado_ML/`](./03_Modelado_ML/) | Regresión lineal, regularización, clustering, ARIMA |
| 4 | [`04_Redes_Neuronales/`](./04_Redes_Neuronales/) | MLP global, LSTM Argentina, comparación ML vs DL |
| 5 | [`05_Storytelling/`](./05_Storytelling/) | Capstone narrativo: las 4 preguntas centrales y sus respuestas |

Si querés ir directo al **cierre del proyecto**, abrí la [Etapa 5 — Informe Final](./05_Storytelling/). El [HTML](./05_Storytelling/05_informe_final.html) es histórico y no refleja la conciliación DR-3. Protocolo, cifras y límites medidos: [validación neuronal](./docs/neural-validation.md).

---

## 🔍 Hallazgos destacados

- **Regresión global, dos protocolos tabulares.** En 4.1, MLP Medio registró R² 0.9796 frente a Ridge 0.7349; en 4.4.A (holdout aleatorio por filas), MLP Medio R² 0.9264 ± 0.0103 en tres seeds frente a Ridge 0.7568. El análisis histórico del cociente `energía_Mtoe / población` es una hipótesis interpretativa, no prueba de que la red haya aprendido esa operación ni de un efecto causal.

- **Las renovables "computables" subestiman la matriz limpia.** La Ley 27.191 solo contabiliza hidroeléctricas pequeñas (≤50 MW), por lo que represas como El Chocón quedan fuera del ratio renovable oficial. Para evaluar la matriz energética completa hay que distinguir explícitamente entre "renovables Ley 27.191" y "fuentes limpias totales" — un matiz importante a la hora de comparar Argentina con otros países.

- **Forecasting 2018, dos ejecuciones distintas.** En 4.3, selección por validación 2017 dio MAPE de test 20.43 ± 0.10% (tuneada, 3 seeds), 20.74% (simple) y 26.68% (ARIMA). La alternativa histórica fija de 4.4.B no reproduce ese tuning: 20.70 ± 3.47%, frente a 20.61% (simple) y 26.68% (ARIMA). Son diferencias descriptivas, no evidencia de superioridad estadística.

---

## 📊 Datos utilizados

| CSV generado por el código de Etapa 2 | Libros de entrada según el ETL | Uso |
|---|---|---|
| `dataset_global.csv` | DS2 (energía mundial) + DS3 (PBI per cápita) + DS4 (población) | Modelado supervisado (Etapas 3 y 4.1) |
| `dataset_argentina_anual.csv` | DS1 (factor de emisión) + DS5 (generación y demanda) + variables de Argentina de DS2/DS3/DS4 | Análisis nacional histórico |
| `dataset_argentina_mensual.csv` | DS5 | Series temporales (Etapas 4.2 y 4.3) |
| `dataset_argentina_provincias.csv` | DS5 | Análisis subnacional (formato long) |
| `dataset_argentina_provincias_wide.csv` | DS5 | Análisis subnacional (formato wide) |

Este mapeo describe **el código**, no acredita el origen de los libros ni certifica que los CSV existentes se hayan generado con una descarga verificable. En particular, el ETL no lee el CSV de Our World in Data. El inventario de los **cinco nombres exactos de Excel**, sus hojas, los datos de origen aún DESCONOCIDOS y el procedimiento para verificarlos están en [`datos/originales/README.md`](./datos/originales/README.md). La resolución de rutas está descrita arriba; las afirmaciones de períodos quedan pendientes de otras tareas.

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

Los enlaces a portales de datos son puntos de entrada orientativos; la atribución institucional de los cinco archivos Excel esperados por el ETL sigue sin verificarse (véase [`datos/originales/README.md`](./datos/originales/README.md)).
