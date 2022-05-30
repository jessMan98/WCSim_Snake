# Ejecucion Procesamiento WCSim

1. Ubicarse en la ruta: 
```
cd WCSim/scripts/snakemake
```
2. Crear contenedor sandbox:
```
singularity build --fakeroot --sandbox docker://manu33/wcsim:1.2  
``` 
3. Crear carpeta compartida
```
singularity exec --fakeroot --writable /bin/bash -c "mkdir /home/compartida"
```
Con estos pasos se podran ejecutar los scripts de Snakemake.
___
## Mantained by:
:man_technologist: Jesús Manuel Alemán González.
