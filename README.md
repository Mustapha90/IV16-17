# Proyecto-IV. Guía de tapas

[![Build Status](https://travis-ci.org/Mustapha90/IV16-17.svg?branch=master)](https://travis-ci.org/Mustapha90/IV16-17)

Este proyecto consiste en crear la infraestructura para el alojamiento, funcionamiento y despliegue de una aplicación web. Será el proyecto que se va a desarrollar en la asignatura DAI, curso 2016/17.

## Descripción

Aplicación web que permite a los usuarios encontrar bares a visitar, localizarlos y consultar las tapas que hay disponibles, también se permitirá a los usuarios votar sobre las tapas y bares, registrarse y probablemente hacer reservas.

## Herramientas de dessarrollo:
En principio se usarán las siguientes tecnologías/herramientas:

* Python.
* Framework Django
* SQLite.
* AJAX.
* JQuery.
* Bootstrap
* HTML y CSS

## 3- Integración continua

### Tests
Los tests se han realizado usando la herramienta de tests que viene integrada en Django, importando el módulo TestCase.

```python
from django.test import TestCase
from rango.models import Bares, Tapas
from django.core.urlresolvers import reverse

### Create your tests here.

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

### Herramientas de construcción
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
### Travis

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

# instalar las dependencias
install: 
 make install

# crear la base de datos
before_script: 
 make createdb
 make populate

# ejecutar tests
script: 
 make test
```
**Paso 3**

Añadimos el fichero ``.travis.yml`` a nuestro repositorio y hacemos un push a la rama master

**Paso 4**

Ahora nos vamos a nuestra cuenta de Travis, para ver el resultado de la integración.


## Infrastructura:

En principio, el despliege de la aplicación se realizará en Azure, probablemente usando heroku como PaaS, se añadirán más detalles en los siguientes hitos.

 
