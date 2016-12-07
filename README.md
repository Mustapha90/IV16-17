# Proyecto-IV. Guía de tapas

[![Build Status](https://travis-ci.org/Mustapha90/IV16-17.svg?branch=master)](https://travis-ci.org/Mustapha90/IV16-17)
[![Heroku](http://heroku-badge.herokuapp.com/?app=angularjs-crypto&style=flat)](https://iv1617.herokuapp.com)

Este proyecto consiste en crear la infraestructura para el alojamiento, funcionamiento y despliegue de una aplicación web. Será el proyecto que se va a desarrollar en la asignatura DAI, curso 2016/17.

##Índice

1. [Descripción](#descripción)
2. [Herramientas de desarrollo](#herramientas-de-desarrollo)
3. [Integración continua](#integración-continua)
4. [Despliegue en PaaS - Heroku](#despliegue-en-paas---heroku)
5. [Entorno de pruebas - Docker](#entorno-de-pruebas---docker)


##Descripción

Aplicación web que permite a los usuarios encontrar bares a visitar, localizarlos y consultar las tapas que hay disponibles, también se permitirá a los usuarios votar sobre las tapas y bares, registrarse y probablemente hacer reservas.

##Herramientas de desarrollo
En principio se usarán las siguientes tecnologías/herramientas:

* Python.
* Framework Django
* SQLite.
* AJAX.
* JQuery.
* Bootstrap
* HTML y CSS

##Integración continua

###Tests
Los tests se han realizado usando la herramienta de tests que viene integrada en Django, importando el módulo TestCase.

```python
from django.test import TestCase
from rango.models import Bares, Tapas
from django.core.urlresolvers import reverse

###Create your tests here.

def add_bar(name, views, likes):
    b = Bares.objects.get_or_create(name=name)[0]
    b.views = views
    b.likes = likes
    b.save()
    return b


class TestsBares(TestCase):
    def test_Visitas(self):
        """
                Asegurar que el numero de visitas es siempre positivo
        """
        bar = Bares(name='test',views=-1, likes=0)
        bar.save()
        self.assertEqual((bar.views >= 0), True)

    def test_slug(self):
        """
                Comprobar la creacion de un campo slug
        """

        bar = Bares(name='bar de pepe',views=0, likes=0)
        bar.save()
        self.assertEqual(bar.slug, 'bar-de-pepe')

class TestViews(TestCase):

    def test_views_sin_bares(self):
        """
        Si no hay categorias, mostrar mensaje
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay categorias.")
        self.assertQuerysetEqual(response.context['categories'], [])
     
    def test_view_con_bares(self):
        """
            Comprobr que los bares se muestran correctamente
        """
        add_bar('test',1,1)
        add_bar('temp',1,1)
        add_bar('tmp',1,1)
        add_bar('tmp test temp',1,1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")
        num_cats =len(response.context['categories'])
        self.assertEqual(num_cats , 4)

class TestTapas(TestCase):
	def test_crear_tapa(self):
		b = Bares(name='test',views=-0, likes=0)
		b.save()
		t = Tapas(title="tapa", likes=10, category=b)
		t.save()
		self.assertEqual(t.title,"tapa")
```

Para ejecutarlos:

``$ python manage.py test``

###Herramientas de construcción
Las herramientas de construccion que he creado son:

``populate_rango.py``: Un script que rellena la base de datos.

**Makefile**

Un fichero makefile con el siguiente contenido:

```makefile
# instalar las dependencias
install:
	pip install -r requirements.txt
# lanzar tests
test:
	python manage.py test
#rellenar la base de datos
populate:
	python populate_rango.py
# Lanzar la aplicación 
execute:
	python manage.py runserver
#Crear la base de datos (sqlite3)
createdb:
	python manage.py migrate --noinput
```

**requirements.txt**

Un fichero que contiene las dependencias de la aplicación

```
Django==1.7
django-registration-redux==1.2
```
###Travis

Para la integracion continua he elegido Travis, ya que es el que ha recomiendado el profesor, además es muy popular y fácil de usar.

Para añadir la integración continua a nuestro repositorio seguimos los siguientes pasos:

**Paso 1**

En nuestra cuenta de Travis, activamos la integración continua para nuestro repositorio.

**Paso 2**

Creamos el fichero ``.travis.yml`` con el siguiente contenido:

```yml
language: python
python:
  - "2.7"

#instalar las dependencias
install: 
 - make install

#crear la base de datos
before_script: 
 - make createdb
 - make populate

#ejecutar tests
script: 
 - make test
```
**Paso 3**

Añadimos el fichero ``.travis.yml`` a nuestro repositorio y hacemos un push a la rama master

**Paso 4**

Ahora nos vamos a nuestra cuenta de Travis, para ver el resultado de la integración.


##Despliegue en PaaS - Heroku

Como PaaS se ha elegido Heroku porque es muy fácil de usar, tiene una documentación muy buena, ofrece hasta cinco aplicaciónes y además permite usar PostgreSQL, todo esto sin ningún coste!

###Separación de entornos

Antes estabamos trabajando en un entorno de desarrollo/pruebas ahora se añade otro entorno, que es el entorno de producción (Heroku), antes usabamos sqlite3, en Heroku no podemos usarla, tenemos que usar PostgreSQL, otro problema que surge es que la configuración de las variables de entorno va a ser distinta, por ejemplo en un entorno de desarrollo, necesitamos activar el modo depuración, mientras en un PaaS la opción de depuración debe estar desactivada.

Además las dependencias son diferentes en los dos entornos, y no tiene sentido usar el mismo fichero ``requirements.txt`` en Travis y en Heroku, estaremos instalando librerías que no se van a usar.


####Separación de los archivos de configuración

Crearemos diferentes ficheros de configuración para cada entorno:

``common_settings.py`` Contentrá la configuración común a los dos entornos

``dev_settings.py`` Contentrá la configuración específica al entorno de desarrollo/pruebas

``settings.py`` Contentrá la configuración específica al entorno de producción

Los dos ficheros de configuración de entornos "heredan" del fichero ``common_settings.py``

Por defecto se trabajaŕa con la configuración de producción ya que más adelante vamos a configurar el despliegue automático con nuestro repositorio github.

En el entorno de desarrollo trabajaremos con una base de datos ``sqlite3`` y tendremos el modo depuración activado

Contenido del fichero ``dev_settings.py``

```python
# -*- coding: utf-8 -*-

from .common_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dz(#w(lfve24ck!!yrt3l7$jfdoj+fgf+ru@w)!^gn9aq$s+&y'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Para trabajar con la configuración de desarrollo hacemos:

``export DJANGO_SETTINGS_MODULE="tango_with_django_project.dev_settings"``

También podemos añadir la linea anterior al final del fichero ``bin/activate`` del entorno virtualenv donde trabajamos para no tener que hacerlo cada vez que lanzamos el shell.

####Separación de las dependencias de cada entorno

Antes teníamos un fichero de depencencias ``requirements.txt``, este fichero lo vamos a dejar para Heroku, y crearemos otro fichero que contendrá las dependencias de desarrollo ``dev_requirements.txt``

###Preparación de la app para el despliegue

####Configuración del contenido estático

Hay que añadir la configuración correcta para que nuestra aplicación podrá servir contenido estático en el Paas.

Para lograrlo usaremos ``whitenoise``, editamos el fichero ``wsgi.py`` de nuestro proyecto

```python
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
```

Añadimos la siguiente linea en el fichero de configuración ``common_settings.py``

```python
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
```

####Configuración de las variables de entorno

Para configurar las variables de entorno en el PaaS usaremos los paquetes python-decouple y dj-database-url.

Editamos el fichero de configuración de producción:

```python
# -*- coding: utf-8 -*-

# Importar la configuración común
from .common_settings import *

from decouple import config
import dj_database_url

# Configuramos la variable de entorno secret_key en el Paas
SECRET_KEY = config('SECRET_KEY')

# Configuramos la variable de entorno de depuración
DEBUG = config('DEBUG', default=False, cast=bool)

# Configuramos la variable de entorno DATABASE_URL que será configurada por Heroku al crear la base de datos Postgres
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

#Permitir el acceso al host de heroku
ALLOWED_HOSTS = [".herokuapp.com"]
```

###Ficheros de configuración del PaaS

Para desplegar la aplicación necesitamos los siguientes ficheros de configuración:

``requirements.txt``

Contiene las dependencias necesarias para el despliegue en el PaaS

```
Django==1.7
django-registration-redux==1.2
whitenoise
dj-database-url==0.3.0
python-decouple==3
dj-static==0.0.6
gunicorn==19.6.0
psycopg2==2.6.1
```

**``runtime.txt``**

Contiene la versión de python necesaria para ejecutar la aplicación

```
python-2.7.12
```

**``Procfile``**

Contiene la orden que se usará para ejecutar la aplicación

```
web: gunicorn tango_with_django_project.wsgi --log-file -
```

###Despliegue en Heroku

Ya tenemos la configuración necesaria para desplegar la aplicación en heroku.

-Creamos la app en Heroku especificando la región y el nombre de la app

``$ heroku apps:create --region eu appiv``

-Creamos la base de datos

``$ heroku addons:create heroku-postgresql:hobby-dev``

-Creamos una variable de entorno que indica que el entorno es Heroku

``$ heroku config:set ON_HEROKU=1``

-Creamos la variable de entonro SECRET_KEY en Heroku

``$ heroku config:set SECRET_KEY=`openssl rand -base64 32` ``

-Iniciamos el despliegue de la aplicación

``$ git push heroku master``

-Creamos las tablas de la base de datos

``$ heroku run python manage.py migrate --noinput``

-Rellenamos la base de datos

``$ heroku run python populate_db.py``

-Ya podemos ver el resultado del despliegue ingresando la url de nuestra aplicación en Heroku o ejecutando:

``$ heroku open``

La aplicación se encuentra desplegada en el siguiente enlace:

[![Heroku](http://heroku-badge.herokuapp.com/?app=angularjs-crypto&style=flat)](https://iv1617.herokuapp.com)

### Actualización de la configuración de Travis

Actualizamos el fichero ``.travis.yml`` para que la integración continua funcione correctamente con los cambios que hemos hecho.

```
language: python
python:
  - "2.7"

# Antes de instalar, exportar la variable de entorno para trabajar con la configuración de desarrollo
before_install:
  - export DJANGO_SETTINGS_MODULE=tango_with_django_project.dev_settings

# instalar las dependencias de desarrollo
install: 
 - make install_dev

# crear la base de datos
before_script: 
 - make migrate
 - make populate

# ejecutar tests
script: 
 - make test
```

Actualizamos el Makefile:

```
# instalar las dependencias de desarrollo/test
install_dev:
	pip install -r dev_requirements.txt

#Crear la base de datos
migrate:
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput
    
#rellenar la base de datos
populate:
	python populate_db.py

# lanzar tests
test:
	python manage.py test

# Lanzar la aplicación 
run:
	python manage.py runserver

# Desplegar la aplicación en Heroku
deploy:
	heroku apps:create --region eu
	heroku addons:create heroku-postgresql:hobby-dev
	heroku config:set ON_HEROKU=1
	heroku config:set SECRET_KEY=`openssl rand -base64 32`
	git push heroku master
	heroku run python manage.py migrate --noinput
	heroku run python populate_db.py
	heroku open
```

### Integración del despliegue automático con el repositorio en GitHub

Para automatizar el inicio del despliegue cuando hacemos un ``push`` a la rama master de nuestro repositorio, nos vamos al dashboard de Heroku, activamos el despliegue automático, y marcamos la opción ``Wait for CI`` para que heroku espere que la integración continua termine antes de desplegar la aplicación.

![Imagen 1](http://i1210.photobucket.com/albums/cc420/mj4ever001/hito31.png)

### Despliegue automático desde local

Para probar el despliegue desde local, hay que tener instalados [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) y [Heroku-CLI](https://devcenter.heroku.com/articles/heroku-command-line)

**Clonamos el repositorio en local**

``$ git clone https://github.com/Mustapha90/IV16-17.git``

``$ cd IV16-17``

**Lanzamos el despliegue usando la herramienta ``make``**

``$ make deploy``

##Entorno de pruebas - Docker

Docker permite crear infraestructuras reproducibles que permiten aislar la ejecución de aplicaciones lo que hace más fácil los procesos de prueba y despliegue.

La imagen se ha creado usando un fichero [Dockerfile](https://github.com/Mustapha90/IV16-17/blob/master/Dockerfile) y un script [docker_entrypoint.sh](https://github.com/Mustapha90/IV16-17/blob/master/docker_entrypoint.sh) que funciona como punto de entrada al contenedor.

La imagen del proyecto se puede encontrar en el siguiente [repositorio de Docker Hub](https://hub.docker.com/r/mustapha90/iv16-17/) que está configurado con el repositorio de GitHub para construir la imagen automáticamente, consulte el siguiente enlace para obtener más información:

[Configure automated builds from GitHub](https://docs.docker.com/docker-hub/github/)

###Uso

Para disponer del entrorno y probarlo hay que seguir estos pasos:

####Instalar Docker

``wget -qO- https://get.docker.com/ | sh``

####Descargar la imagen

``sudo docker pull mustapha90/iv16-17``

####Arrancar el contenedor

La aplicación depende de dos variables de entorno ``SECRET_KEY`` que es una clave secreta (El usuario puede usar cualquiera), y ``DATABASE_URL``, que es la URL de la base de datos remota, estas variables hay que pasarlas al contenedor usando el siguiente comando.

``sudo docker run -e "SECRET_KEY=<Clave_Secreta>" -e "DATABASE_URL=<Enlace_BD>" -i -t mustapha90/iv16-17``

####Lanzar la aplicación

``make docker_run``

Para visualizar la aplicación desde un navegador del sistema anfitrión introducimos la siguiente dirección:

``http://<IP>:8000/``

Donde ``<IP>`` es La dirección IP del contenedor que se puede obtener ejecutando el comando ``ifconfig``
