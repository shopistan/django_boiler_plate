"""
Django settings for test environment.
"""
import os

from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3(5qle3-j_2^6gx1jlgnd8)k0_v(qle3-j_2^6gx1w*qle3-j_2^6gx1$r@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

HOST = os.environ.get('HOST')
ADMIN_URL = "http://"+HOST+"/"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testDatabase',
    }
}
