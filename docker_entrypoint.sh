#!/bin/bash

# Crear las tablas de la base de datos
make migrate

#Rellenar la base de datos
make populate

#Preparar los ficheros estáticos necesarios para el despliegue
make staticfiles

#Imprimir la dirección IP del contenedor para permitir el acceso externo
echo "$(tput setaf 3)IP del contenedor:  $(tput setaf 6)$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')$(tput sgr 0)"

#Para Lanzar la aplicación
printf "\nPara Lanzar la aplicación:\nmake docker_run\n"

#Lanzar tests
make test

#Lanzar el shell, esto permite que permanacer dentro del contenedor
/bin/bash

