# Django settings for DOWNSIZE project	

#get relative references right
import os, sys
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


#DEBUG settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('downsizer', 'jonathan.s.sheller@gmail.com'),
    ('Jon', 'jonathan.s.sheller@gmail.com'),
    ('Kelly', 'kshachett@gmail.com'),
    ('Gregg', 'gregg.m.rubin@gmail.com'),
)

MANAGERS = ADMINS

#DATABASE settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dsdb2',                      # Or path to database file if using sqlite3.
        'USER': 'jonsheller',                      # Not used with sqlite3.
        'PASSWORD': 'cookiemonster77',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

#
# **** Right now, static file and media both point to the same place (so that references in templates won't break). at some point, make media point to user-uploaded items and make static point to OUR static items
#

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# ****  Media URL and Static URL may not be right, they are now REVERSED

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# carryover from file system change. not sure what this does or where it is referenced
BASE_URL = 'http://jonandkelly.webfactional.com/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9kog0q2nq=u5d($2jusn%*da##k%5^fjx#1(9@k62gw7+&87va'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
# removed, but should reactivate    'django.middleware.csrf.CsrfViewMiddleware',
# removed, but should reactivate    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', #should be for django-authentication (i think)
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'dsenv.ds.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),  #main template folder
)


# ALL template context processors - brought over from other file system... 
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    #"django.core.context_processors.static",       #error when this line is included
    "django.contrib.messages.context_processors.messages",
    "django_facebook.context_processors.facebook",
)

# ALL auth bacends brought over from dsold
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_facebook.auth_backends.FacebookBackend',
)

#from dsold
REGISTRATION_BACKEND = 'registration.backends.default.DefaultBackend'

# from dsold. facebook API config items
FACEBOOK_API_KEY = '51de1f7266a48cbfb4803f318f3c2560'
FACEBOOK_APP_ID = '115188795231633'
FACEBOOK_APP_SECRET = '3c0696334ad840299d34e22e2a4f8b62'

INSTALLED_APPS = (
    'django.contrib.auth', 			#default
    'django.contrib.contenttypes', 		#default
    'django.contrib.sessions', 			#default
    'django.contrib.sites', 			#default
    'django.contrib.messages', 			#default
    'django.contrib.staticfiles', 		#default
    'django_extensions', 			#extensions pack
    		# Uncomment the next line to enable the admin:
    'django.contrib.admin', 			#default
    		# Uncomment the next line to enable admin documentation:
    'registration',				#handles registration backend
    'relationships',				#enables various relationships
    'django_facebook',				#facebook integration (sort of works)
    'django.contrib.humanize',			#formatting stuff
    'ds.goals',				#USER custom app
    'ds.account',			#USER custom app
    'ds.info',				#USER custom app
    'ds.charities',			#USER custom app
    #not used now 'ds.networks',			#USER custom app
    'django.contrib.admindocs', 		#default
    #'south',  					not using now
)

#data for debug toolbar
INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

#from dsold
# configuration settings for django-registration auth backend
# may not work since we will no longer be logged in to webfactional!
ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'jonandkelly'
EMAIL_HOST_PASSWORD = 'k311ysh'
DEFAULT_FROM_EMAIL = 'administrator@jonandkelly.webfactional.com'
SERVER_EMAIL = 'administrator@jonandkelly.webfactional.com'
LOGIN_REDIRECT_URL = '/'

# from dsold
# i think this is a part of the above settings
AUTH_PROFILE_MODULE = 'account.UserProfile'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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
