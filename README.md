# Ejecucion Procesamiento WCSim

1. Ubicarse en la ruta: WCSim/scripts/snakemake y crear contenedor sandbox:
singularity build --fakeroot --sandbox docker://manu33/wcsim:1.2

2. Crear carpeta compartida
singularity exec --fakeroot --writable /bin/bash -c "mkdir /home/compartida"

Con estos 2 pasos se podran ejecutar los scripts de Snakemake.
