from .base import *


DEBUG = True

ADMINS = [
    ('Phil Gyford', 'phil@gyford.com'),
]

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     get_env_variable('DB_NAME'),
        'USER':     get_env_variable('DB_USERNAME'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST':     get_env_variable('DB_HOST'),
        'PORT':     '',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# If you *don't* want to prepend www to the URL, remove the setting from
# the environment entirely. Otherwise, set to 'True' (or anything tbh).
# PREPEND_WWW = False


CACHES = {
    'default': {
        # Use dummy cache (ie, no caching):
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',

        # Or use in-memory cache:
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'pepysdiary',

        # Or use local memcached:
        #'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        #'LOCATION': '127.0.0.1:11211',
        #'TIMEOUT': 500, # millisecond
    }
}

# Debug Toolbar settings.
if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    INSTALLED_APPS += ['debug_toolbar', ]
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        # Force the toolbar to show as INTERNAL_IPS wasn't working with Vagrant.
        'SHOW_TOOLBAR_CALLBACK': "%s.true" % __name__
    }
    INTERNAL_IPS = ['127.0.0.1', '192.168.33.1', '0.0.0.0']
    RESULTS_CACHE_SIZE = 100

    # Stop Django handling static files in favour of Whitenoise.
    # (When DEBUG = False)
    # Need to add the app just before staticfiles, so:
    new_apps = []
    for app in INSTALLED_APPS:
        if app == 'django.contrib.staticfiles':
            new_apps.append('whitenoise.runserver_nostatic')
        new_apps.append(app)
    INSTALLED_APPS[:] = new_apps


    def true(request):
        return True


#############################################################################
# PEPYSDIARY-SPECIFIC SETTINGS.

GOOGLE_ANALYTICS_ID = 'UA-89135-2'

# From https://www.google.com/recaptcha/
RECAPTCHA_PUBLIC_KEY = get_env_variable('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = get_env_variable('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_USE_SSL = True

# Do we use Akismet/TypePad spam checking?
# True/False. If false, no posted comments are checked.
# If True, AKISMET_API_KEY must also be set.
USE_SPAM_CHECK = True

# From http://akismet.com/
AKISMET_API_KEY = get_env_variable('AKISMET_API_KEY')

# From http://mapbox.com/
MAPBOX_MAP_ID = 'philgyford.hnhb28lo'
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoicGhpbGd5Zm9yZCIsImEiOiJUUGpZME9zIn0.O3bxMZ-0-Fq-e0HwR6-xcA';
