# Django settings for testappa project.
import os
from os.path import abspath, basename, dirname, join, normpath
from sys import path

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

path.append(DJANGO_ROOT)

BASE_DIR = SITE_ROOT

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': SITE_ROOT + '/app.db',                   # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# Additional locations of static files

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'custom_static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^8@%x2*-v!w14+6x56kj*^k_j2+41yql%)o7%1=apr*-375%oe'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
#    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
    # 'social.backends.google.GoogleOAuth2',
    'testappa.backends.GluuOidc',
    'django.contrib.auth.backends.ModelBackend', # this is default
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'testappa.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'testappa.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'app',
    'bootstrap_base',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)


SOCIAL_AUTH_GLUU_OIDC_KEY = os.getenv('SOCIAL_AUTH_GLUU_OIDC_KEY',
                                      b'@!DA85.5F98.95A1.CA3B!0001!5FD3.3646!0008!FD9F.7302')
SOCIAL_AUTH_GLUU_OIDC_SECRET = os.getenv('SOCIAL_AUTH_GLUU_OIDC_SECRET',
                                         b'see env var')

ACCESS_TOKEN_METHOD = os.getenv('ACCESS_TOKEN_METHOD', 'POST')

BASE_OIC_URL = os.getenv('BASE_OIC_URL', 'https://idp.texaspass.org')

BASE_API_URL = os.getenv('BASE_API_URL', 'http://admin.texaspass.org/api/')

DEFAULT_SCOPE = ['openid', 'profile', 'email', 'teainfo']

USER_FIELDS_CLAIMS_MAP = [
    ('organization', 'teaDistrictID'),
    ('school', 'teaCampusID'),
    ('username', 'sub'),
    ('state_id', 'teaStudentStateUniqueID'),
    ('sis_id', 'teaDistrictUsername'),
    ('person_id', 'teaDistrictPersonIdentifier'),
    ('staff_id', 'teaStaffUniqueStateID'),
    ('grade', 'teaGrade'),
    ('first_name', 'given_name'),
    ('middle_name', 'teaMiddleName'),
    ('last_name', 'sn'),
    ('common_name', 'cn'),
    ('date_of_birth', 'teaDateOfBirth'),
    ('role', 'teaRole'),
]
#SOCIAL_AUTH_GLUU_OIDC_AUTH_EXTRA_ARGUMENTS = {'prompt': 'consent'}

AUTH_USER_MODEL = 'app.TeaUser'
USER_MODEL = AUTH_USER_MODEL
LOGIN_URL = '/login/gluu-oidc/'
LOGIN_REDIRECT_URL = '/protected/'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
