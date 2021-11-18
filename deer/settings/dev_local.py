from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = True

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'SECRET_KEY')

# Todo: DB setting.... 