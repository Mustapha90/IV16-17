#!/bin/bash

make migrate
make populate
make staticfiles
echo "$(tput setaf 3)IP del contenedor:  $(tput setaf 6)$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')$(tput sgr 0)"
printf "\nPara Lanzar la aplicación:\nmake docker_run\n"
/bin/bash

