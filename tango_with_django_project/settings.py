# -*- coding: utf-8 -*-

# Importar la configuracion comun
from .common_settings import *

from decouple import config
import dj_database_url

EN_DOCKER = os.getenv('EN_DOCKER')

if 'DYNO' in os.environ:
: #Si se ejecuta en Heroku
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

elif EN_DOCKER:
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dffvilk1d8s44b',
        'USER': 'xwskwpqbdialqo',
        'PASSWORD': 'za9l3xiwVmAAVZ5_mKDgaWyjyE',
        'HOST': 'ec2-54-75-233-92.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
        }
     }
    DEBUG = False
    SECRET_KEY = 'Hola'
    ALLOWED_HOSTS = ['*']


