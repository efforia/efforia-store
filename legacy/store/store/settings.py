from __future__ import absolute_import, unicode_literals
import os

SHOP_CHECKOUT_FORM_CLASS = 'store.forms.ExternalPaymentOrderForm'
SHOP_CHECKOUT_STEPS_SPLIT = True
SHOP_CHECKOUT_STEPS_CONFIRMATION = False
SHOP_CURRENCY_LOCALE = 'ptb' if 'posix' not in os.name else 'pt_BR.UTF-8'
SHOP_HANDLER_BILLING_SHIPPING = 'store.hooks.sedex_shipping_handler'
SHOP_HANDLER_TAX = None
SHOP_HANDLER_ORDER = None
SHOP_HANDLER_PAYMENT = 'store.hooks.multiple_payment_handler'

EXTRA_MODEL_FIELDS = ((
    'cartridge.shop.models.Order.paypal_redirect_token',
    'django.db.models.CharField',(),{
        'blank': True,
        'null': True,
        'max_length': 36
    }),(
    'cartridge.shop.models.Order.pagseguro_redirect',
    'django.db.models.CharField',(),{
        'blank': True,
        'null': True,
        'max_length': 200
    })
)

USE_SOUTH = True
SITE_TITLE = 'Efforia Nanocomputadores'
JQUERY_FILENAME = 'jquery-1.7.1.min.js'
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
ADMINS = ()
MANAGERS = ADMINS
ALLOWED_HOSTS = ['*']
TIME_ZONE = 'America/Sao_Paulo'
USE_TZ = True
LANGUAGE_CODE = 'pt-BR'
_ = lambda s: s
LANGUAGES = (
	('pt-BR', _('Brazilian Portuguese')),
	('en', _('English'))
)
DEBUG = True if 'posix' not in os.name else False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SITE_ID = 1
USE_I18N = True
INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

AUTHENTICATION_BACKENDS = (
    'mezzanine.core.auth_backends.MezzanineBackend', 
    'django.contrib.auth.backends.ModelBackend'
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

FILE_UPLOAD_PERMISSIONS = 420
DATABASES = {}

if 'posix' not in os.name:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dev.db',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': ''
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'efforia',
            'USER': 'efforia',
            'PASSWORD': 'mk28to#$',
            'HOST': '127.0.0.1',
            'PORT': ''
        }
    }
    CACHE_MIDDLEWARE_SECONDS = 60
    CACHE_MIDDLEWARE_KEY_PREFIX = 'efforia'
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                  'LOCATION': '127.0.0.1:11211'}}
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True
}

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]
if 'posix' not in os.name: CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if 'posix' not in os.name else os.path.abspath('store')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, *STATIC_URL.strip('/').split('/'))
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'public'),)
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip('/').split('/'))
ROOT_URLCONF = 'store.urls'
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)

INSTALLED_APPS = (
    'django.contrib.admin', 
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.redirects', 
    'django.contrib.sessions', 
    'django.contrib.sites', 
    'django.contrib.sitemaps', 
    'django.contrib.staticfiles', 
    'cartridge.shop', 
    'mezzanine.boot', 
    'mezzanine.conf', 
    'mezzanine.core', 
    'mezzanine.generic', 
    'mezzanine.blog', 
    'mezzanine.forms', 
    'mezzanine.pages', 
    'mezzanine.galleries', 
    'mezzanine.twitter', 
    'mezzanine.accounts',  
    'shipping',
    'store', 
    #'south', 
    'gunicorn'
)

EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff','.svg'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm'],
    'Document': ['.pdf','.doc','.rtf','.txt','.xls','.csv'],
    'Audio': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    'Code': ['.html','.py','.js','.css']
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'mezzanine.conf.context_processors.settings',
    'mezzanine.pages.context_processors.page'
)

MIDDLEWARE_CLASSES = (
    'mezzanine.core.middleware.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cartridge.shop.middleware.ShopMiddleware',
    'mezzanine.core.request.CurrentRequestMiddleware',
    'mezzanine.core.middleware.TemplateForDeviceMiddleware',
    'mezzanine.core.middleware.TemplateForHostMiddleware',
    'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware',
    'mezzanine.pages.middleware.PageMiddleware',
    'mezzanine.core.middleware.FetchFromCacheMiddleware'
)

PACKAGE_NAME_FILEBROWSER = 'filebrowser_safe'
PACKAGE_NAME_GRAPPELLI = 'grappelli_safe'

OPTIONAL_APPS = (
    'debug_toolbar',
    'django_extensions',
    'compressor',
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI
)

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
SECRET_KEY = '928f26e4-2b36-48c1-b9b7-5e2049306018df5334a2-3efa-4de8-a10b-010226b85823eaa7584f-0878-43f2-b099-45f4b73519af'
NEVERCACHE_KEY = '0085b0ee-8947-4699-ba15-6bbf538cf75f06e504a2-ee28-4c9e-8a23-ffa5bdebc69384f3b8c4-e63f-4c95-874f-d43f59ff92aa'
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

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
