# DR-4: transacción de paquete (preparación, no publicación)

La raíz del repositorio es la fuente de diez notebooks, cinco CSV limpios, `requirements.txt` y dos documentos de `docs/`. El directorio intermedio medido aporta exactamente dos CSV. El script genera un README navegable, la nota sobre originales ausentes y un PDF y DOCX legibles a partir de `docs/executive-summary.md`. El manifiesto explícito en `scripts/prepare_delivery_package.py` es la lista cerrada de destinos; no se sincronizan directorios completos. Los HTML y notebooks exclusivos del paquete no se tocan: sus HTML son históricos. No se copian libros Excel, ni se produce video o enlace de entrega.

Desde la raíz del repositorio, inspeccionar primero SIN escrituras:

```sh
python3 -B scripts/prepare_delivery_package.py --dry-run --package-root '/ruta/Entregables DPDS' --backup-root '/ruta/externa/nueva-backup' --intermediate-root '/ruta/stage/datos/intermedios'
```

La salida JSON contiene destino, acción, SHA-256, tamaño y huella original si hay colisión; comparar nombres y capacidad antes de cualquier aprobación. `--repo-root` puede fijar explícitamente otra raíz fuente. El backup debe ser externo al paquete y estar ausente o vacío. Ni `--dry-run` ni la ausencia de `--apply` crean carpetas. Aplicación requiere una autorización independiente y explícita (NO se ejecutó al preparar esta transacción):

```sh
python3 -B scripts/prepare_delivery_package.py --apply --package-root '/ruta/Entregables DPDS' --backup-root '/ruta/externa/nueva-backup' --intermediate-root '/ruta/stage/datos/intermedios'
```

Antes de promover un byte se preparan todos los artefactos, se releen las copias de staging, se guardan todas las colisiones bajo `backup/originals/` y se verifican sus huellas. `backup/manifest.json` describe los destinos y la regla de reversión. Cada destino se prepara como archivo temporal hermano y se promueve con `os.replace`; la reversión de una colisión también se prepara y reemplaza de ese modo. Se limpian los temporales ante excepciones y se verifica cada destino tras promoverlo. Esto es atómico **por archivo**, no para la transacción completa: durante la aplicación pueden convivir destinos viejos y nuevos. Si una promoción falla, se restauran las colisiones promovidas desde backup y se eliminan solo los archivos nuevos incluidos en la lista; se conservan los demás archivos del paquete. Si una reversión falla, la excepción `ROLLBACK FAILED` exige intervención manual; NO volver a aplicar a ciegas. Una interrupción abrupta del proceso (apagado, kill) no activa la reversión automática: la recuperación manual sigue siendo necesaria. Utilizar el manifiesto y las copias externas para restaurar originales, comparando SHA-256 y tamaño, retirar únicamente destinos `create` que se hayan creado durante la operación y revisar posibles temporales hermanos antes de intervenir. No borrar ni sobrescribir archivos ajenos al manifiesto. Conservación del backup corresponde al operador.

Para readback manual, contrastar cada `sha256` y `size` del manifiesto con los bytes del destino, y cada `original_sha256` con `backup/originals/<destino>`. Comprobar que `resumen_ejecutivo.docx` se abre como ZIP OOXML y que el PDF muestra el texto; las pruebas automatizadas inspeccionan ambas estructuras con la biblioteca estándar. Repetir una corrida exige un backup nuevo vacío y nueva inspección de cambios. No ejecutar la etapa ETL desde esta entrega: faltan cinco originales Excel. Los notebooks con outputs almacenados y los HTML existentes pueden contener resultados históricos: consultar `docs/neural-validation.md`.
