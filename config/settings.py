"""
Django settings for w4e project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('W4E_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('W4E_DEBUG') == 'True':
    DEBUG = True
else:
    DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Application definition

INSTALLED_APPS = (
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sentinel',
)

# Registration package setup
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1
LOGIN_REDIRECT_URL = "/sentinels/list/"


# Postmark email setup
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY')
POSTMARK_SENDER = 'dane@dacxl.com'
DEFAULT_FROM_EMAIL = POSTMARK_SENDER
POSTMARK_TEST_MODE = False
POSTMARK_TRACK_OPENS = False

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'w4e_prod',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
}

import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Add a project level template file
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'with_date': {
            'format': '%(asctime)s %(levelname)s; %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s w4e %(levelname)s: %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'with_date',
        },
        'SysLog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'simple',
            'address': ('logs2.papertrailapp.com', 55691)
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'SysLog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'w4e': {
            'handlers': ['file', 'SysLog'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
