# Instalación de Azure-CLI y configuración de credenciales

En este tutorial se explicará como instalar ``Azure-CLI`` y configurar las credenciales para poder asministrar los servicios ofrecidos por Microsoft Azure como la creación de máquinas virtuales, de manera automática usando herramientas como Vagrant.

## Instalación de Azure-CLI

Instalamos ``Azure-CLI`` con los siguientes comandos:

```
$ apt-get install nodejs-legacy
$ apt-get install -y npm
$ npm install -g azure-cli
```

## Configuración de credenciales

Azure-CLI funciona en dos modos ``arm`` (Resource Manager) y ``asm`` (Administración de servicios)
Nosotros vamos a trabajar en el modo ``asm``

``$ azure config mode asm``

Ahora nos identificamos con:

``$ azure login``

El comando anterior nos genera una clave y un enlace a una página web donde debemos introducir esta clave para identificarnos

Ahora descargamos las credenciales:

``$ azure account download``

Accedemos al enlace generado por el comando anterior y descargamos el fichero de credenciales

Importamos el fichero de credenciales descargado a Azure-CLI

``$ azure account import <credentials.publishsettings>``

Borramos el fichero anterior ya que contiene información sensible y no lo vamos a necesitar.

Para conectarnos con Azure necesitamos generar un par de certificados.

```
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout azure_key.pem -out azure_key.pem
$ chmod 600 azure_key.pem
$ openssl x509 -inform pem -in azure_key.pem -outform der -out azure_key.cer
```

Subimos el fichero ``azure_key.cer`` a nuestra [cuenta de Azure](https://manage.windowsazure.com/), en el apartado configuración --> CERTIFICADOS DE ADMINISTRACIÓN.

Por último, obtenemos el identificador de nuestra subscripción en Azure: 

``$ azure account list``

Apuntamos el id de la subscripción con la que vamos a trabajar.

Ya hemos terminado, con el fichero ``azure_key.pem`` y el id de subscipción que hemos obtenido, podemos crear máquinas virtuales usando Vagrant.
