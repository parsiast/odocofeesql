# odosql/settings/production.py
from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ["185.8.172.51", "odocoffee.ir"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
    }
}

STATIC_ROOT = "/var/www/odosql/static/"


CORS_ALLOWED_ORIGINS = [
    "https://odocoffee.ir",
    "http://odocoffee.ir",
    "http://185.8.172.51:80",
    "https://185.8.172.51:80",
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")