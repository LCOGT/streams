"""
Django settings for your TOM project with the tom_education plugin.
"""

import os
import sys
import tempfile

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=z125%(yc62o36iz90jl73#hbd6pet_gy%e%=hf7#ccqg7(9!)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'guardian',
    'tom_common',
    'django_comments',
    'bootstrap4',
    'crispy_forms',
    'django_filters',
    'django_gravatar',
    'django_dramatiq',
    'tom_education',
    'tom_targets',
    'tom_alerts',
    'tom_catalogs',
    'tom_observations',
    'tom_dataproducts',
    'tom_astrosource',
    'corsheaders'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tom_common.middleware.ExternalServiceMiddleware',
]

ROOT_URLCONF = 'streams.urls'

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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'streams.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:m:s'
DATE_FORMAT = 'Y-m-d'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '_static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'data')
MEDIA_URL = '/data/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}

# Caching
# https://docs.djangoproject.com/en/dev/topics/cache/#filesystem-caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': tempfile.gettempdir()
    }
}

# TOM Specific configuration
TARGET_TYPE = 'SIDEREAL'

FACILITIES = {
    'LCO': {
        'portal_url': 'https://observe.lco.global',
        'api_key': os.environ.get('PORTAL_TOKEN',''),
    },
}

TOM_ALERT_CLASSES = [
    'tom_alerts.brokers.mars.MARSBroker',
    'tom_alerts.brokers.lasair.LasairBroker',
    'tom_alerts.brokers.scout.ScoutBroker',
]

EXTRA_FIELDS = [
    {'name': 'active', 'type': 'boolean'},
    {'name': 'target_info', 'type': 'string', 'hidden': True},
]

# Authentication strategy can either be LOCKED (required login for all views)
# or READ_ONLY (read only access to views)
AUTH_STRATEGY = 'READ_ONLY'

# URLs that should be allowed access even with AUTH_STRATEGY = LOCKED
# for example: OPEN_URLS = ['/', '/about']
OPEN_URLS = []

HOOKS = {
    'target_post_save': 'tom_common.hooks.target_post_save',
    'observation_change_state': 'tom_common.hooks.observation_change_state'
}

DATA_TYPES = (
    ('SPECTROSCOPY', 'Spectroscopy'),
    ('PHOTOMETRY', 'Photometry')
)

TOM_FACILITY_CLASSES = [
    'tom_observations.facilities.lco.LCOFacility',
    'tom_education.facilities.EducationLCOFacility'
]

TOM_EDUCATION_TIMELAPSE_SETTINGS = {
    'format': 'gif',
    'fps': 10,
    'size': 500,
}

TOM_EDUCATION_TIMELAPSE_GROUP_NAME = 'Good quality data'

TOM_EDUCATION_PIPELINES = {
    'astrosource': 'tom_astrosource.models.AstrosourceProcess'
}

# Example Dramatiq configuration using Redis on localhost:6379
DRAMATIQ_BROKER = {
    'BROKER': 'dramatiq.brokers.redis.RedisBroker',
    'OPTIONS': {'url': 'redis://localhost:6379'},
    'MIDDLEWARE': [
        'dramatiq.middleware.AgeLimit',
        'dramatiq.middleware.TimeLimit',
        'dramatiq.middleware.Callbacks',
        'dramatiq.middleware.Retries',
        'django_dramatiq.middleware.DbConnectionsMiddleware',
    ]
}

AUTO_THUMBNAILS = False

THUMBNAIL_MAX_SIZE = (0, 0)

THUMBNAIL_DEFAULT_SIZE = (200, 200)

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:5000',
# ]

CORS_ORIGIN_ALLOW_ALL = True

try:
    from local_settings import * # noqa
except ImportError:
    pass
