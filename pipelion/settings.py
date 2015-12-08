"""
Django settings for pipelion project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vg2-nd0_-c=^+@c5f-2r7-^91_r^u4_=!9sgvl5%yb=9=wh*8%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rapid',
    'djgeojson',
    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'pipelion.urls'

WSGI_APPLICATION = 'pipelion.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', 
        'NAME': 'rapid',  # Name of your spatial database
        'USER': 'postgres',   # Database user 
        'PASSWORD': 'mineral3condition',# Database password 
        'HOST': '127.0.0.1',
        'PORT': '5432',   
    }
}


# UNIX
GEOS_LIBRARY_PATH = '/home/dotproj/djangostack-1.7.8-0/postgresql/lib/libgeos_c.so'
GDAL_LIBRARY_PATH = '/home/dotproj/djangostack-1.7.8-0/postgresql/lib/libgdal.so'
GDAL_DATA = '/home/dotproj/djangostack-1.7.8-0/postgresql/share/gdal'

# OS X
# GEOS_LIBRARY_PATH = '/Applications/djangostack-1.6.10-0/postgresql/lib/libgeos_c.dylib'
# GDAL_LIBRARY_PATH = '/Applications/djangostack-1.6.10-0/postgresql/lib/libgdal.dylib'
# GDAL_DATA = '/Applications/djangostack-1.6.10-0/postgresql/share/gdal' 




# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
