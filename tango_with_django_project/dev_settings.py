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






