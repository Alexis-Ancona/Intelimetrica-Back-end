from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['alexis-intelimetrica.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd2oq6faqtcoh0',
        'HOST': 'ec2-54-211-176-156.compute-1.amazonaws.com',
        'USER': 'uozjiqzusawzyc',
        'PORT': 5432,
        'PASSWORD': '5aedc2db6094cbdbe926d1ef034310229379678ec45f9c69ae26add62e338768',
    }
}