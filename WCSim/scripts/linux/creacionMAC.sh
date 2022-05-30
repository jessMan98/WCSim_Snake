#!/bin/bash

# Para la ejecución del script, cambiar la ruta de la linea 5, 8, 9, 10 a la ruta de la máquina local.

cd /home/many/Descargas/MCA_AutoSC-main/Crear_MAC

echo "Eliminando archivos .mac anteriores..."
rm -r /home/many/Descargas/MCA_AutoSC-main/data/1_MAC/VaryE/mu-/*.mac
rm -r /home/autosc/Descargas/MCA_AutoSC-main/data/1_MAC/VaryE/e-/*.mac
rm -r /home/autosc/Descargas/MCA_AutoSC-main/data/1_MAC/VaryE/gamma/*.mac

echo "Creando archivos .mac con particula mu-"
python3 mac_files_config.py -i 12 --config_json config_mu.json -d ../data/1_MAC/VaryE/mu-

echo "Creando archivos .mac con particula e-"
python3 mac_files_config.py -i 12 --config_json config_e.json -d ../data/1_MAC/VaryE/e-

echo "Creando archivos .mac con particula gamma"
python3 mac_files_config.py -i 12 --config_json config_gamma.json -d ../data/1_MAC/VaryE/gamma
