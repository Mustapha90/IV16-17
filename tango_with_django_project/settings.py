# -*- coding: utf-8 -*-

# Importar la configuracion comun
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

