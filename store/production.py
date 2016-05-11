from store.settings import *

DEBUG = False

# PostgreSQL Connection for Django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'efforia',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432'
    }
}
