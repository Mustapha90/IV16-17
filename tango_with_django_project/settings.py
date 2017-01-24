# -*- coding: utf-8 -*-

# Importar la configuracion comun
from .common_settings import *

from decouple import config
import dj_database_url

EN_DOCKER = os.getenv('EN_DOCKER')
ON_HEROKU = 'ON_HEROKU' in os.environ

# Si estamos en Heroku
if ON_HEROKU:  
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
    ALLOWED_HOSTS = ["*"]

elif EN_DOCKER:
    DATABASES = {
          'default': dj_database_url.config(
          default=config('DATABASE_URL')
          )
    }
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALLOWED_HOSTS = ['*']
