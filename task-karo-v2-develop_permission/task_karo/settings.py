"""
Django settings for task_karo project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

from decouple import config
import firebase_admin
from firebase_admin import initialize_app,credentials

import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$0=pwtl=10a1hwyxm998^c_!t*ba0viqo(f-(dgl6nor^%&uah'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',True)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'adminlte3',
    'adminlte3_theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
    'drf_yasg',
    'storages',
    "django_crontab",
    "fcm_django",
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
]

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(days=100),
# }



# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ],
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }

#FIREBASE_APP = initialize_app()
cred = credentials.Certificate(BASE_DIR / 'serviceAccountKey.json')
firebase_admin.initialize_app(cred)

CRONJOBS = [
    # ('0 9 * * *', 'django.core.management.call_command', ['userjourney_time']),
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'task_karo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'task_karo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_EXPIRE = 2592000
AWS_S3_OBJECT_PARAMETERS = {
     'CacheControl': 'max-age=2592000',
}
AWS_LOCATION = 'media'
AWS_QUERYSTRING_AUTH =False
PUBLIC_MEDIA_LOCATION = 'media'
AWS_DEFAULT_ACL='public-read'
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')

REST_FRAMEWORK = { 
   'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' 
#'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH':False
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'USER_ID_FIELD': 'pk'
}



DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': config('DB_NAME'),
         'USER':config('DB_USER_NAME'),
         'PASSWORD': config('DB_PASSWORD'),
         'HOST': config('DB_HOST'),
         'PORT': '5432',
     }
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5 MB

APPEND_SLASH=True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators





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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'api.User'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [(BASE_DIR / 'static')]


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
SITE_ID = 1

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# RazorPay Settings
RAZORPAY_API_KEY = config('RAZORPAY_API_KEY')
RAZORPAY_API_SECRET = config('RAZORPAY_API_SECRET')

# TEXTLOCAL_API_KEY = 'NjI3MzM1NDc3YTcwNjY0YzUyNjU1MjczMzYzNzZjNTQ='

# REST_FRAMEWORK = {
#     # 'DEFAULT_AUTHENTICATION_CLASSES': (
#     #     'rest_framework.authentication.TokenAuthentication',
#     # ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_THROTTLE_CLASSES': (
#         'rest_framework.throttling.AnonRateThrottle',
#     ),
#     'DEFAULT_THROTTLE_RATES': {
#         'anon': '30/sec',
#     },
# }
# REST_FRAMEWORK = {
#  'DEFAULT_FILTER_BACKENDS': ('rest_framework_timedelta.filters.TimedeltaFilterBackend', )
# }

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }

# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
# EMAIL_HOST_USER = '<Gmail Id>' 
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587 
# EMAIL_USE_TLS = True 
# EMAIL_HOST_PASSWORD = "<Password>"