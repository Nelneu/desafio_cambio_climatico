# Validación neuronal DR-3 (evidencia de ejecución aislada)

Corridas medidas en CPU con Python 3.12, TensorFlow 2.21.0, NumPy 2.5.3 y pandas 3.0.6. `jinja2>=3.1.5` es dependencia directa de `pandas .style` (faltó en el primer intento de 4.3). Estas métricas son observaciones de notebooks ejecutados, no pruebas de origen de los datos.

| Ejecución | Protocolo | Resultado observado |
|---|---|---|
| 4.1 | Regresión global, MLP Medio, split por filas | R² 0.9796 frente a Ridge R² 0.7349 (CSV exportado) |
| 4.4.A | Regresión global, holdout aleatorio por filas; MLP Medio seeds 42, 123, 2024 | R² 0.9264 ± 0.0103 frente a Ridge R² 0.7568 |
| 4.3 | Serie mensual: entrenamiento 2011–2016, validación recursiva 2017 para elegir E4/E5/E6; luego reentrenamiento pre-2018 y test 2018 una vez | Elegidos batch_size 32, lr 5e-4, sin regularización; LSTM tuneada seeds 42, 123, 7: MAPE 20.43 ± 0.10%, MAE 72.75 ± 0.34 GWh, RMSE 107.93 ± 0.27 GWh. LSTM simple MAPE 20.74% y ARIMA(1,1,1) 26.68% en ese test. |
| 4.4.B | Comparador independiente con configuración histórica fija (bs=4, lr=5e-3), **no reproduce** la configuración seleccionada en 4.3; mismo año de test pero otra ejecución | Alternativa MAPE 20.70 ± 3.47% (seeds 42, 123, 7); simple 20.61% frente a ARIMA 26.68%. |

Los desvíos son entre tres seeds, no intervalos de confianza. Los números entre ejecuciones no son intercambiables; diferencias de MAPE no demuestran superioridad estadística. El split tabular aleatorio por fila puede compartir países y años entre entrenamiento y prueba: no evalúa países o años inéditos. La serie tiene solo 96 meses y el test solo 12; no se infieren causas ni desempeño futuro. Los HTML y outputs guardados en los notebooks fuente no fueron regenerados; pueden mostrar cifras históricas. 4.4.C consolida A y B medidos, **no** incluye la configuración de 4.3 en su ranking.

Evidencia privada temporal (no copiar datasets al repositorio): `/tmp/dr3-mlp-VUkR2XXQ/stage/datos/intermedios/resultados_paso_4_1_mlp_regresion.csv`, `/tmp/dr3-5vq8rcsk/04_redes_neuronales_paso4_3.executed.ipynb`, `/tmp/dr3-rest-wpNqJb8W/04_redes_neuronales_paso4_4_A.executed.ipynb` y `04_redes_neuronales_paso4_4_B.executed.ipynb` en ese mismo directorio. Son rutas efímeras, no archivos de entrega.

Para repetir, en una **copia aislada** con los CSV limpios disponibles, instalar `requirements.txt`, definir `CLIMATE_PROJECT_ROOT` a esa copia y ejecutar secuencialmente con un kernel Python 3.12, por ejemplo `jupyter nbconvert --to notebook --execute --output 04_redes_neuronales_paso4_3.executed.ipynb 04_redes_neuronales_paso4_3.ipynb`; ejecutar 4.1, 4.4.A y 4.4.B del mismo modo, conservando los resultados solo en el staging privado. No se hizo un nuevo entrenamiento para redactar esta nota.
