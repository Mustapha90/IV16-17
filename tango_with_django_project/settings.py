# -*- coding: utf-8 -*-

from .common_settings import *

from decouple import config
import dj_database_url

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

ALLOWED_HOSTS = [".herokuapp.com"]

