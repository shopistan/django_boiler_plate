"""
Django settings for developement environment.
"""
import os

from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9h@ni#i3g+@@&7mj5qle3-j_2^6gx13(5jlgnd8)k0_v(w*$r@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

HOST = os.environ.get('HOST')
ADMIN_URL = "https://"+HOST+"/"

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_ADDRESS,
        'PORT': DB_PORT,
        'CONN_MAX_AGE': 0
    }
}

