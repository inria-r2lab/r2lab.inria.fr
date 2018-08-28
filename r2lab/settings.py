"""
Django settings for r2lab project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os, os.path

# import r2lab.sitesettings as sitesettings
#
# from .sitesettings import (
#     SECRET_KEY,
#     ALLOWED_HOSTS,
#     DEBUG,
# )
#


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#################### figure out if in production mode or not
import socket
PRODUCTION = 'r2lab' in socket.gethostname()

# the directory where we have write access to store the db and other logs
RUNTIME_DIR = '/var/lib/r2lab.inria.fr' if PRODUCTION else BASE_DIR

# use same location - rather than /var/log - for permissions
# on r2lab.inria.fr we have a a symlink in place in /var/log as well
LOG_FILE = os.path.join(RUNTIME_DIR, "django.log")

from .logger import init_logger
logger = init_logger(LOG_FILE)

########## details on the R2lab API

### PLC API endpoint for creating a PlcApiProxy
# relevant only if testbed_api == 'plcapi':
plcapi_settings = {
    'url' : 'https://r2labapi.inria.fr:443/PLCAPI/',
    # this of course should be owned by group apache and in mode 0440
    'credentials' : [
        '/etc/rhubarbe/plcapi.credentials',
        'r2lab/plcapi.credentials',
    ],
    # xxx doublecheck this one
    'nodename_match' : 'faraday',
}

####################

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '07k3$-3qn2zmpss0rrb#c0h-t#wqc#9&gx2eqr)oaydb5ruued'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'r2lab.inria.fr',
    'localhost',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
# third party stuff
    ### we call the markdown library ourselves, no need for this django app yet
    #'markdown_deux',
    ### for running a https devel server
    # pip3 install django-sslserver
    # uncomment sslserver line below, and then run with
    # manage.py runsslserver --certificate ../sidecar/localhost.crt --key ../sidecar/localhost.key
    # 'sslserver',
# local stuff
    ###
    # md is our own brew for displaying web pages written in markdown
    # it will serve http://<>/md/foo{,.md,.html} by searching for markdown/foo.md
    'md.apps.MdConfig',
    'mfauth.apps.MfauthConfig',
    'leases.apps.LeasesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'r2lab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR + '/templates' ],
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

WSGI_APPLICATION = 'r2lab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(RUNTIME_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/assets/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]

manifold_url = "https://portal.onelab.eu:7080/"

# IMPORTANT NOTE.
# not specifying either http: or https: here is the right thing to do
# it means to use the same protocol as the one
# used to reach the main service in the first place
sidecar_url = "//r2lab.inria.fr:999/"

if not PRODUCTION:
    # use remote sidecar, unless SIDECAR is defined
    # it can be either the actual sidecar_url,
    # or e.g. 'local', to use the default hardwired in sidecar.js
    SIDECAR = os.getenv('SIDECAR')
    if not SIDECAR:
        # development mode with no setting: use the local sidecar
        sidecar_url = "http://localhost:10000"
    elif 'http' in SIDECAR:
        # development mode, SIDECAR mentions http, this means
        # it points at the URL to use
        sidecar_url = SIDECAR_URL
    else:
        # development mode, SIDECAR defined to e.g. r2lab
        # specify https
        sidecar_url = "https://r2lab.inria.fr:999/"
    print("Using sidecar_url = {sidecar_url}".format(**locals()))

# transitioning to plcauthbackend
AUTHENTICATION_BACKENDS = (
    'plc.plcauthbackend.PlcAuthBackend',
    'mfauth.mfbackend.ManifoldBackend',
)

X_FRAME_OPTIONS = 'ALLOWALL'
