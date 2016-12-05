#!/bin/bash

make migrate
echo "$(tput setaf 3)IP del contenedor: $(tput setaf 6)$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')$(tput sgr 0)"
