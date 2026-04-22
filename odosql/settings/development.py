# odosql/settings/development.py
from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ["*","127.0.0.1", "localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME',"odosql"),
        'USER': os.environ.get('DB_USER',"root"),
        'PASSWORD': os.environ.get('DB_PASSWORD',"@Parsia1377"),
        'HOST': os.environ.get('DB_HOST',"127.0.0.1"),
        'PORT': os.environ.get('DB_PORT',"3306"),
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173"
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS



