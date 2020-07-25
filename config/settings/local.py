"""
Django settings for local environment.
"""
import os

from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j5qle3-j_2^6gx13(9h@ni#le3-j_2^6gi5jlgnd8)k0_v(w*$r@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

HOST = os.environ.get('HOST')
ADMIN_URL = "http://"+HOST+"/"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'HOST': DB_ADDRESS,
        'PORT': DB_PORT,
        'CONN_MAX_AGE': None

    }
}