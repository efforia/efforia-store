""" Invent General Settings for Django """
from __future__ import absolute_import, unicode_literals
import os

SHOP_CHECKOUT_FORM_CLASS = 'invent.forms.ExternalPaymentOrderForm'
SHOP_CHECKOUT_STEPS_SPLIT = True
SHOP_CHECKOUT_STEPS_CONFIRMATION = False
#SHOP_CURRENCY_LOCALE = 'ptb' if 'posix' not in os.name else 'pt_BR.UTF-8'
SHOP_CURRENCY_LOCALE = 'en_US.UTF-8'
#SHOP_HANDLER_BILLING_SHIPPING = 'invent.hooks.sedex_shipping_handler'
SHOP_HANDLER_BILLING_SHIPPING = None
SHOP_HANDLER_TAX = None
SHOP_HANDLER_ORDER = None
#SHOP_HANDLER_PAYMENT = 'invent.hooks.multiple_payment_handler'
SHOP_HANDLER_PAYMENT = None


USE_SOUTH = True
SITE_TITLE = 'Efforia Nanocomputadores'
JQUERY_FILENAME = 'jquery-1.8.3.min.js'
LOCALE_DATE = ('Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dec')
STORE_POSTCODE = '90020110'
STORE_COUNTRY = 'Brasil'
BANK_AGENCY = '1430-3'
BANK_ACCOUNT = '33640-8'
BANK_SOCIALNAME = 'EFFORIA TECNOLOGIA LTDA - ME'
PAYPAL_SANDBOX_MODE = False
PAYPAL_SANDBOX_RECEIVER_EMAIL = 'efforiaca-facilitator@gmail.com'
PAYPAL_SANDBOX_CLIENT_ID = 'AeiijxAGPGKJ1J94r7u7nqX_8oCKtOzI0ZNChSIMwAkEg2Y3wff8FQhPfGZw'
PAYPAL_SANDBOX_CLIENT_SECRET = 'EKmSiRBgd31RKZ324o47--u1IgxoOMI-J6UvuIP-X5qFSm30xYy_ULllqHIc'
PAYPAL_RECEIVER_EMAIL = 'efforiaca@gmail.com'
PAYPAL_CLIENT_ID = 'AcuUFhDe6YARWq5at2cdaoLQHsH2koobgx1xId97sIx7vBrRGqC9fH2tpO_V'
PAYPAL_CLIENT_SECRET = 'ELcuGBAvIYa70j611-Tm9KJcVVymhutA-hwOhQNGMPXiBjH7YyDvSsxJjCGl'
PAGSEGURO_SANDBOX_MODE = False
PAGSEGURO_SANDBOX_EMAIL_COBRANCA = 'contato@efforia.com.br'
PAGSEGURO_SANDBOX_TOKEN = 'FB7093D836BD40F6AB3DF509FECE1ED0'
PAGSEGURO_EMAIL_COBRANCA = 'efforiaca@gmail.com'
PAGSEGURO_TOKEN = 'D9BBC61094BB4C8BADB296613350FF20'
SHOP_CURRENCY = 'BRL'
DEFAULT_HOST = 'www.efforia.com.br'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'contato@efforia.com.br'
EMAIL_HOST_PASSWORD = 'c40k21_1'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
TIME_ZONE = 'America/Sao_Paulo'
USE_TZ = True
LANGUAGE_CODE = 'pt-br'
_ = lambda s: s
LANGUAGES = (
    ('pt-br', _('Brazilian Portuguese')),
    ('es-ar', _('Argentinian Spanish')),
    ('en', _('English'))
)
DEBUG = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SITE_ID = 1
USE_I18N = True
INTERNAL_IPS = ('127.0.0.1')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

FILE_UPLOAD_PERMISSIONS = 420

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "efforia.db"
    }
}

CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = 'efforia'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True
}

BASE_DIR = PROJECT_ROOT = os.path.abspath('')
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_ROOT.split(os.sep)[-1]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'invent/static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'invent/public'),
)
MEDIA_URL = STATIC_URL + 'media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip('/').split('/'))
ROOT_URLCONF = 'invent.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'invent/templates')],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.tz',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ]
        }
    }
]

INSTALLED_APPS = (
    'flat_responsive',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    # 'shipping',
    'invent',
)

EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.svg'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'],
    'Code': ['.html', '.py', '.js', '.css']
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
SECRET_KEY = '928f26e4'
NEVERCACHE_KEY = '0085b0ee'
SSH_USER = 'azureuser'
FABRIC = {
    'SSH_USER': SSH_USER,
    'SSH_PASS': 'mk28to#$',
    'SSH_KEY_PATH': '',
    'HOSTS': ['factory.efforia.com.br'],
    'VIRTUALENV_HOME': '/home/%s' % SSH_USER,
    'PROJECT_NAME': 'efforia',
    'REQUIREMENTS_PATH': 'requirements.txt',
    'GUNICORN_PORT': 8000,
    'LOCALE': 'pt_BR.UTF-8',
    'LIVE_HOSTNAME': 'factory.efforia.com.br',
    'REPO_URL': 'git@factory.efforia.com.br:efforia.git',
    'DB_PASS': 'mk28to#$',
    'ADMIN_PASS': 'mk28to#$',
    'SECRET_KEY': SECRET_KEY,
    'NEVERCACHE_KEY': NEVERCACHE_KEY
}

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
ANONYMOUS_USER_ID = -1
