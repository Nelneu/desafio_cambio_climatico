# Datos originales — inventario y trazabilidad pendiente

Esta carpeta documenta los cinco libros que espera `02_Limpieza/02_limpieza_transformacion.ipynb` (DS1–DS5). Los nombres y las hojas siguientes están **confirmados por el código**, no por una descarga comprobada. No hay un registro de origen verificable para estos archivos: el enlace exacto de descarga, la entidad editora, la versión o revisión, la fecha de publicación y la suma SHA-256 de **cada libro** son DESCONOCIDOS. El nombre de un archivo, sus columnas y una página institucional no demuestran su procedencia.

## Inventario de entradas y salidas según el ETL

Los nombres son literales: respetar tildes, guiones, mayúsculas y las extensiones `.xls`/`.xlsx`. Para ejecutar 01 y 02, colocar estos cinco archivos en `datos/originales/` bajo la raíz del proyecto. Los notebooks buscan la raíz desde el directorio de trabajo actual hacia arriba (debe contener `README.md` y `datos/`); fuera de ese árbol, definir `CLIMATE_PROJECT_ROOT` con la ruta de la raíz, por ejemplo tras montar Drive en Colab (`drive.mount('/content/drive')`). El override se valida y las entradas ausentes dan error explícito; no se buscan reemplazos. La Etapa 2 exporta los CSV a `datos/limpios/`, sin acreditar por ello la procedencia de los libros.

| ID | Libro esperado (nombre exacto) | Hoja consumida y lectura confirmada | Destino en el código |
|---|---|---|---|
| DS1 | `Emisio_n_CO2_en_Argentina.xlsx` | `FACTOR DE EMISION OM SIMPLE`; `skiprows=5`, columnas 1–3: año y factores ex-post/ex-ante. | `dataset_argentina_anual.csv` (factor de emisión). |
| DS2 | `Estadísticas_energía_mundial.xlsx` | `CO2 emissions from fuel combus` → `co2_MtCO2`; `Share of renewables in electri` → `share_renewables`; `Electricity production` → `electricity_TWh`; `Total energy consumption` → `energy_Mtoe`; `Share of wind and solar in ele` → `share_wind_solar`. Se leen esas cinco hojas con `header=None` y años en la tercera fila. | `dataset_global.csv`; su fila de Argentina aporta variables a `dataset_argentina_anual.csv`. |
| DS3 | `PBI_per_cápita_-_datos_Banco_Mundial.xls` | Primera hoja por defecto (`sheet_name` no especificado); `skiprows=3`, encabezados en la siguiente fila; PBI per cápita. | `dataset_global.csv` y, por esa vía, `dataset_argentina_anual.csv`. |
| DS4 | `Población_mundial_-_dataset_Banco_Mundial.xlsx` | Primera hoja por defecto (`sheet_name` no especificado); misma función de carga que DS3; población. | `dataset_global.csv` y, por esa vía, `dataset_argentina_anual.csv`. |
| DS5 | `Proyectos_renovables_en_Argentina.xlsx` | Primera hoja por defecto (`sheet_name` no especificado); `header=None`, encabezados de la segunda fila; energía generada, fuente, mes, provincia y registros `Demanda MEM`. | `dataset_argentina_anual.csv`, `dataset_argentina_mensual.csv`, `dataset_argentina_provincias.csv` (formato long) y `dataset_argentina_provincias_wide.csv` (formato wide). |

El código une DS2 + DS3 + DS4 por país y año para el conjunto global; integra DS1, DS5 y variables globales de Argentina para el conjunto anual. Los conjuntos mensual y provinciales proceden de DS5. La celda de exportación escribe **cinco CSV** en `datos/limpios/`; no se afirma que los CSV existentes en `datos/limpios/` se hayan regenerado o que coincidan bit a bit con una ejecución nueva.

## Enlaces orientativos, no prueba de origen

- [Our World in Data — repositorio CO₂](https://github.com/owid/co2-data): punto de entrada para consultar otras series; **`owid-co2-data.csv` no figura como entrada del ETL** y no sustituye DS2.
- [Secretaría de Energía — datos abiertos](https://www.energia.gob.ar/datos-abiertos), [CAMMESA — informe mensual](https://cammesaweb.cammesa.com/informe-mensual/) e [INDEC](https://www.indec.gob.ar/): puntos de búsqueda, **no enlaces verificados de descarga de DS1 o DS5** ni prueba de que esas entidades publicaran estos libros exactos.
- El texto «Banco Mundial» en los nombres DS3/DS4 y la estructura de las columnas tampoco verifican una descarga, serie, edición o publicador concretos. Los enlaces anteriores no acreditan los cinco libros.

**Estado para DS1, DS2, DS3, DS4 y DS5:** URL exacta de descarga: DESCONOCIDA; editor institucional y cadena de custodia: NO VERIFICADOS; identificador de serie y versión/revisión: DESCONOCIDOS; fecha de publicación o actualización: DESCONOCIDA; checksum SHA-256 del archivo fuente: DESCONOCIDO. No se atribuye a una institución concreta ninguno de esos archivos sin el registro correspondiente.

## Cómo cerrar la verificación de cada libro

1. Localizar una ficha de recurso o repositorio del editor con URL **directa al archivo exacto** (no solo a la página principal). Conservar la URL de la ficha, la URL final tras redirecciones y, si existe, identificador de recurso/serie.
2. Descargar solo el archivo pertinente y registrar editor tal como figura en la ficha, fecha de publicación/actualización, versión o revisión y fecha de acceso. Si un dato no consta, anotarlo como desconocido en vez de inferirlo del nombre.
3. Registrar el nombre original y el nombre local usado para el ETL, tamaño y SHA-256 calculado sobre los bytes descargados (por ejemplo, `sha256sum nombre-del-archivo.xlsx`); conservar evidencia de la ficha y de cualquier renombrado.
4. Comparar hojas, encabezados y columnas del inventario con el libro real y anotar el resultado. Una coincidencia estructural no prueba por sí sola la procedencia. Solo después de verificar los cinco registros se podrá afirmar reproducibilidad de una ejecución desde fuentes originales.

Plantilla **sin completar**, una copia por cada uno de los cinco libros (no es evidencia de una descarga):

```text
ID (DS1–DS5):
Nombre exacto esperado por el ETL:
Nombre original descargado y motivo del renombrado, si aplica:
Editor indicado por la ficha (o DESCONOCIDO):
Título e identificador de recurso/serie (o DESCONOCIDO):
URL de la ficha y evidencia archivada (o DESCONOCIDA):
URL exacta de descarga y URL final tras redirecciones (o DESCONOCIDAS):
Versión/revisión y fecha de publicación/actualización (o DESCONOCIDAS):
Fecha de acceso/descarga (o DESCONOCIDA):
Tamaño en bytes y SHA-256 del archivo descargado (o DESCONOCIDOS):
Hojas y encabezados comparados con el ETL; resultado:
Responsable de la verificación y observaciones:
```

Hasta entonces, los libros no son recuperables de forma reproducible a partir de los enlaces orientativos. Las afirmaciones de períodos o tamaños en otros documentos y vistas HTML requieren verificación por separado; no se corrigen en esta tarea.
