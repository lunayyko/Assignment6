from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'SECRET_KEY')

DATABASES = {
    'default' : {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': os.environ.get('SQL_DATABASE', 'deer'),
        'USER': os.environ.get('SQL_USER', 'user-deer'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password-deer'),
        'HOST':  os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', 3306),
        'OPTIONS' : {
            'charset' : 'utf8mb4'
        }
    }
}