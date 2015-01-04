"""
Django settings for studying_mandarin_chinese project.

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
SECRET_KEY = 'kkia$mp*#pni-_y58l7)h&1+)fg#qj7-wf()ssf-u7!c1o0g5*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vocabulary',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'studying_mandarin_chinese.urls'

WSGI_APPLICATION = 'studying_mandarin_chinese.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

# -----------------------------------------
#  SQLAlchemy and VCAP_SERVICES
# -----------------------------------------
from sqlalchemy import create_engine
import json

engine = [0]

def initialize():
    #
    # If a local VCAP_SERVICES.json file is found,
    # use it as a config file. (local env)
    # If not, read from an env variable. (on BlueMix)
    #
    try:
        conf = open(BASE_DIR + '/VCAP_SERVICES.json', 'r')
        vcap_config = conf.read(1024)
        conf.close()
    except IOError:
        vcap_config = os.environ.get('VCAP_SERVICES')

    print vcap_config

    decoded_config = json.loads(vcap_config)
    for key, value in decoded_config.iteritems():
         if key.startswith('postgres'):
             pgsql_creds = decoded_config[key][0]['credentials']
    pgsql_uri = str(pgsql_creds['uri'])

    print pgsql_uri
    engine[0] = create_engine(pgsql_uri)
