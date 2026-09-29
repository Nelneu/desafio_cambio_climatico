# Resumen ejecutivo: cambio climático y energías renovables

## Alcance

El estudio describe una muestra seleccionada de 16 países entre 1990 y 2018 y series de Argentina. La muestra no representa a todos los países. Las asociaciones observadas entre emisiones, energía y variables socioeconómicas no establecen causalidad ni permiten atribuir efectos a políticas públicas.

## Resultados de regresión global

En 4.1, con división por filas, MLP Medio obtuvo R² 0.9796 y Ridge R² 0.7349. En la ejecución independiente 4.4.A, con holdout aleatorio por filas, MLP Medio obtuvo R² 0.9264 ± 0.0103 entre tres semillas y Ridge R² 0.7568. Estas cifras corresponden a protocolos diferentes; no son estimaciones intercambiables. Países y años pueden aparecer tanto en entrenamiento como en prueba: no se midió generalización a países o años inéditos. Las variaciones entre semillas no son intervalos de confianza.

## Serie temporal de Argentina

En 4.3 se seleccionó la configuración con validación recursiva de 2017 sobre entrenamiento 2011–2016, se reentrenó con datos anteriores a 2018 y se evaluó una vez sobre 2018. La LSTM ajustada registró MAPE 20.43 ± 0.10%, MAE 72.75 ± 0.34 GWh y RMSE 107.93 ± 0.27 GWh entre tres semillas. La LSTM simple registró MAPE 20.74% y ARIMA(1,1,1) 26.68% en esa ejecución. La alternativa fija 4.4.B es otra ejecución, no la configuración seleccionada en 4.3. Doce meses de prueba no demuestran una ventaja estadística ni desempeño futuro.

## Límites de entrega

Los cinco CSV limpios y dos resultados intermedios permiten consultar los análisis procesados. No se incluyen los cinco libros Excel originales: la limpieza desde fuentes crudas no es reproducible solo con este paquete. Los HTML existentes son instantáneas históricas y pueden contener rutas o cifras obsoletas; consultar notebooks fuente y docs/neural-validation.md para protocolo y límites. Estos resultados no prueban eficacia de despliegues ni de intervenciones públicas.
