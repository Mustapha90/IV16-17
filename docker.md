#Entorno de pruebas - Docker

##Creación de la imagen

La imagen se ha creado usando un fichero Dockerfile y un script docker_entrypoint.sh que funciona como punto de entrada al contenedor.

**Dockerfile**

```
FROM ubuntu:14.04
MAINTAINER Mustapha Mayo <mj4ever001@gmail.com>

#Variable de entorno que indica que estamos en docker
ENV EN_DOCKER=true

#Instalar dependencias
RUN sudo apt-get -y update
RUN sudo apt-get install -y git
RUN sudo apt-get install -y build-essential python-setuptools python-dev libpq-dev
RUN sudo easy_install pip
RUN sudo pip install --upgrade pip

#Clonar el repositorio del proyecto
RUN sudo git clone https://github.com/Mustapha90/IV16-17.git

#Cambiar el directorio de trabajo al directorio del proyecto
WORKDIR IV16-17

#Instalar dependencias del proyecto
RUN make install_prod

#Permitir el acceso externo al puerto 8000 que será usado por la aplicación
EXPOSE 8000

#Punto de entrada, este script se ejecuta automáticamente al iniciar el contenedor
ENTRYPOINT ["./docker_entrypoint.sh"]
```

**docker_entrypoint.sh**

```
#!/bin/bash

# Crear las tablas de la base de datos
make migrate

#Rellenar la base de datos
make populate

#Lanzar tests
make test

#Preparar los ficheros estáticos necesarios para el despliegue
make staticfiles

#Imprimir la dirección IP del contenedor para permitir el acceso externo
echo "$(tput setaf 3)IP del contenedor:  $(tput setaf 6)$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')$(tput sgr 0)"

#Para Lanzar la aplicación
printf "\nPara Lanzar la aplicación:\nmake docker_run\n"

#Lanzar el shell, esto permite que permanacer dentro del contenedor
/bin/bash
```

##Construcción automatizada de la imagen

Para construir la imagen automáticamente desde GitHub, creamos un repositorio en DockerHub, en el panel pulsamos Create y elegimos create automated build, a partir de este punto el proceso se puede realizar siguiendo las instrucciones de nos facilita dockerhub


##Prueba del entorno

Descargamos la imagen:

``sudo docker pull mustapha90/iv16-17``

Lanzamos el contenedor pasandole las variables de entorno SECRET_

````










