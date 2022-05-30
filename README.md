# Procesamiento WCSim con Snakemake y Singularity Container

## Creación Archivos Mac

1. Ubicarse en la ruta donde se descargo el repositorio y entrar a la siguiente carpeta:
```
cd WCSim_Snake/WCSim/scripts/linux
```
2. Cambiar permisos al archivo:  **creacionMAC.sh**
```
sudo chmod +x creacionMAC.sh
```
3. Ejecutar archivo:
```
./creacionMAC.sh
```
4. Visualizar el resultado en la siguiente ruta: 

```
cd ../../data/1_MAC/VaryE/{particula}
```
  Donde {particula} = _/e-_ , _/gamma_ , _/mu-_

___

## Ejecución Scripts Snakemake

1. Ubicarse en la ruta: 
```
cd WCSim/scripts/snakemake
```
2. Crear contenedor sandbox:
```
singularity build --fakeroot --sandbox wcsim/ docker://manu33/wcsim:1.2  
``` 
3. Crear carpeta compartida
```
singularity exec --fakeroot --writable /bin/bash -c "mkdir /home/compartida"
```
Con estos pasos se podrán ejecutar los scripts de Snakemake.
___
## Mantained by:
:man_technologist: Jesús Manuel Alemán González.
