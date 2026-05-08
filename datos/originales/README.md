# Datos originales — Fuentes y procedimiento de descarga

> Esta carpeta **no contiene archivos de datos**. Solo este README, que documenta de dónde provienen los datasets utilizados y cómo descargarlos.

---

## 🤔 ¿Por qué no están los datos crudos en el repo?

Por buenas prácticas de ingeniería de datos:

1. **Trazabilidad explícita.** Los datos públicos cambian (correcciones retrospectivas, agregados de años nuevos). Apuntar a la fuente oficial es más fiable que congelar una copia.
2. **Repositorio liviano.** Los archivos originales pesan varios MB y Git no los versiona bien (no hace diffs sobre archivos binarios).
3. **Reproducibilidad.** Cualquiera puede regenerar los datos limpios desde cero siguiendo este README.

Si solo querés **ejecutar los notebooks de Etapa 3 y 4**, no hace falta que descargues nada — los datasets ya procesados están en [`../limpios/`](../limpios/).

---

## 📥 Fuentes utilizadas

### 🌍 Datos globales

#### Our World in Data — CO₂ and Greenhouse Gas Emissions
- **URL:** https://github.com/owid/co2-data
- **Archivo descargado:** `owid-co2-data.csv`
- **Variables tomadas:** emisiones de CO₂ por país y año, población, PBI per cápita, consumo energético per cápita, share de renovables, share de eólica + solar.
- **Cobertura usada en el proyecto:** 16 países seleccionados, 1990–2018.

> **Nota sobre OWID:** este dataset es un archivo unificado que internamente combina varias fuentes:
> - Emisiones de CO₂ → [Global Carbon Project](https://globalcarbonbudget.org/)
> - Datos energéticos → [Energy Institute Statistical Review of World Energy](https://www.energyinst.org/statistical-review) (sucesor del histórico BP Statistical Review)
> - PBI y población → World Bank + Maddison Project Database
>
> Por eso, citar OWID como fuente única es correcto y a la vez respeta la procedencia de cada serie individual.

> ⚠️ **Importante:** el archivo de OWID incluye además agregaciones (por ej. "World", "OECD members", "High income", "Africa"). En la Etapa 2 estas se filtran y se seleccionan los 16 países usados en el análisis.

---

### 🇦🇷 Datos de Argentina

#### Secretaría de Energía de la Nación — Datos Abiertos
- **URL:** https://www.energia.gob.ar/datos-abiertos
- **Datasets utilizados:**
  - Generación eléctrica anual por fuente (1990–presente)
  - Generación eléctrica por provincia (anual, por tipo de fuente)
- **Marco regulatorio relevante:** [Ley 27.191](http://servicios.infoleg.gob.ar/infolegInternet/anexos/255000-259999/258952/norma.htm) — define cuáles fuentes computan como "renovables" (incluye hidro ≤50 MW; excluye grandes represas).

#### CAMMESA — Compañía Administradora del Mercado Mayorista Eléctrico
- **URL:** https://cammesaweb.cammesa.com/informe-mensual/
- **Dataset utilizado:** Informes mensuales del MEM (Mercado Eléctrico Mayorista).
- **Variables tomadas:** generación mensual por fuente renovable (eólica, solar, biomasa, biogás, biodiesel, hidro chica), demanda total del MEM.
- **Cobertura usada:** 96 meses (2017–2024).

#### INDEC — Instituto Nacional de Estadística y Censos
- **URL:** https://www.indec.gob.ar/
- **Indicadores complementarios:** población argentina, PBI nacional.

---

## 🔄 Reproducir los datasets limpios desde cero

Si querés regenerar [`../limpios/`](../limpios/) desde las fuentes:

1. Descargá los archivos según los enlaces de arriba y colocálos en esta carpeta.
2. Abrí el notebook [`../../02_Limpieza/02_limpieza_transformacion.ipynb`](../../02_Limpieza/02_limpieza_transformacion.ipynb).
3. Ejecutalo de principio a fin. Los CSVs limpios se regeneran en `../limpios/`.

---

## 📌 Última verificación de las fuentes

Las URLs y procedimientos descritos fueron verificados en **abril de 2025**. Si alguna URL cambia, las páginas raíz de cada institución (Secretaría de Energía, CAMMESA, INDEC, Our World in Data) son los puntos de entrada estables.
