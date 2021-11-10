# from ..production import *

import os

{% include "insights/apps/insights/settings/partials/common.py" %}

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup

if os.environ.get('ENABLE_DJANGO_TOOLBAR', '').lower() in ('true', 't', '1'):
    INSTALLED_APPS += (
        'debug_toolbar',
    )

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    DEBUG_TOOLBAR_PATCH_SETTINGS = False

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
########## END TOOLBAR CONFIGURATION

LMS_COURSE_SHORTCUT_BASE_URL = 'https://example.com/courses'
CMS_COURSE_SHORTCUT_BASE_URL = 'https://studio.example.com/course'

########## BRANDING
PLATFORM_NAME = 'Open edX'
APPLICATION_NAME = 'Insights'
FULL_APPLICATION_NAME = f'{PLATFORM_NAME} {APPLICATION_NAME}'
########## END BRANDING


# Uncomment the line below to avoid having to worry about course permissions
ENABLE_COURSE_PERMISSIONS = False
########## END AUTHENTICATION/AUTHORIZATION

########## FEEDBACK AND SUPPORT
HELP_URL = '#'
########## END FEEDBACK

########## SEGMENT.IO
# 'None' disables tracking.  This will be turned on for test and production.
SEGMENT_IO_KEY = os.environ.get('SEGMENT_WRITE_KEY')
########## END SEGMENT.IO

LOGGING = get_logger_config(debug=DEBUG, dev_env=True, local_loglevel='DEBUG')

########## END MODULE_PREVIEW

########## REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)
########## END REST FRAMEWORK CONFIGURATION

########## DATA API CONFIGURATION
DATA_API_AUTH_TOKEN = 'edx'
########## END DATA API CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = os.environ.get("ANALYTICS_SECRET_KEY", "insecure-secret-key")
########## END SECRET CONFIGURATION

########## SESSION COOKIE
# See: https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = 'sessionid'
######### END SESSION COOKIE

DB_OVERRIDES = dict(
    PASSWORD=os.environ.get('DB_PASSWORD', DATABASES['default']['PASSWORD']),
    USER=os.environ.get('DB_USER', DATABASES['default']['USER']),
    NAME=os.environ.get('DB_NAME', DATABASES['default']['NAME']),
    HOST=os.environ.get('DB_HOST', DATABASES['default']['HOST']),
    PORT=os.environ.get('DB_PORT', DATABASES['default']['PORT']),
)

for override, value in DB_OVERRIDES.items():
    DATABASES['default'][override] = value

DATA_API_URL = os.environ.get("API_SERVER_URL", 'http://edx.devstack.analyticsapi:19001/api/v0')

# Set these to the correct values for your OAuth2/OpenID Connect provider (e.g., devstack)
SOCIAL_AUTH_EDX_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_KEY', 'insights-sso-key')
SOCIAL_AUTH_EDX_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_SECRET', 'insights-sso-secret')
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_ISSUER', 'http://localhost:18000')
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT', 'http://edx.devstack.lms:18000')
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL', 'http://localhost:18000/logout')
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = os.environ.get(
    'SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT', 'http://localhost:18000',
)

BACKEND_SERVICE_EDX_OAUTH2_KEY = os.environ.get('BACKEND_SERVICE_EDX_OAUTH2_KEY', 'insights-backend-service-key')
BACKEND_SERVICE_EDX_OAUTH2_SECRET = os.environ.get('BACKEND_SERVICE_EDX_OAUTH2_SECRET', 'insights-backend-service-secret')
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = os.environ.get(
    'BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL', 'http://edx.devstack.lms:18000/oauth2',
)

COURSE_API_URL = 'http://edx.devstack.lms:18000/api/courses/v1/'
GRADING_POLICY_API_URL = 'http://edx.devstack.lms:18000/api/grades/v1/'

MODULE_PREVIEW_URL = 'http://edx.devstack.lms:18000/xblock'

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}