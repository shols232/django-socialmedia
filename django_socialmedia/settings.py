"""
Django settings for django_socialmedia project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1', '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # project apps
    'account',
    'post', 
    'chatapp',

    # third party
    'crispy_forms',
    'social_django',
    'django_extensions',
    'emoji',
    'emoji_picker',
    'channels',
    # 'allauth',  
    # 'allauth.account',   
    # 'allauth.socialaccount',   
    # 'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_socialmedia.urls'

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

WSGI_APPLICATION = 'django_socialmedia.wsgi.application'
ASGI_APPLICATION = 'django_socialmedia.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DEBUG = config('DEBUG', default=False, cast=bool)
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default':dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]



CRISPY_TEMPLATE_PACK = 'bootstrap4'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
   'django.contrib.auth.backends.ModelBackend',
#  'allauth.account.auth_backends.AuthenticationBackend',
#  )

# Facebook App ID
# SITE_ID = 1
# LOGIN_REDIRECT_URL = '/'

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
)
SOCIAL_AUTH_FACEBOOK_KEY = '416793205963376' 
SOCIAL_AUTH_FACEBOOK_SECRET = '6f887c723205fc73d87d215db81ffa0d'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '537833100881-16n0qhq5e739d170f4s6t59s25kj6cdp.apps.googleusercontent.com' # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'hxph7Dt1TA3CbXeqw3jODv35' # Google Consum

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  
# EMAIL_USE_TLS = True
# MAILER_EMAIL_BACKEND = EMAIL_BACKEND  
# EMAIL_HOST = 'smtp.gmail.com'  
# EMAIL_HOST_PASSWORD = 'your_password'  
# EMAIL_HOST_USER = 'your_email'  
# EMAIL_PORT = 465  
# EMAIL_USE_SSL = True  
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
