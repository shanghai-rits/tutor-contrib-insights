from ..devstack import *

# import os

{% include "insights/apps/insights/partials/common.py" %}

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
########## END DEBUG CONFIGURATION

ALLOWED_HOSTS = ['*']

ENABLE_AUTO_AUTH = True

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
#     }
# }
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup


INSTALLED_APPS += (
    'debug_toolbar',
)

#     MIDDLEWARE += [
#         'debug_toolbar.middleware.DebugToolbarMiddleware',
#     ]

#     DEBUG_TOOLBAR_PATCH_SETTINGS = False

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
# INTERNAL_IPS = ('127.0.0.1',)
########## END TOOLBAR CONFIGURATION

LMS_COURSE_SHORTCUT_BASE_URL = 'http://{{ LMS_HOST }}/courses'
CMS_COURSE_SHORTCUT_BASE_URL = 'http://{{ CMS_HOST }}/course'

# Uncomment the line below to avoid having to worry about course permissions
ENABLE_COURSE_PERMISSIONS = False
########## END AUTHENTICATION/AUTHORIZATION

########## FEEDBACK AND SUPPORT
HELP_URL = '#'
########## END FEEDBACK

########## SEGMENT.IO
# 'None' disables tracking.  This will be turned on for test and production.
SEGMENT_IO_KEY = "{{ INSIGHTS_SEGMENT_WRITE_KEY }}"
########## END SEGMENT.IO

# LOGGING = get_logger_config(debug=DEBUG, dev_env=True, local_loglevel='DEBUG')

########## END MODULE_PREVIEW

# ########## REST FRAMEWORK CONFIGURATION
# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     'rest_framework.renderers.JSONRenderer',
#     'rest_framework.renderers.BrowsableAPIRenderer',
# )
########## END REST FRAMEWORK CONFIGURATION

########## DATA API CONFIGURATION
DATA_API_AUTH_TOKEN = 'edx'
########## END DATA API CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = "{{ INSIGHTS_SECRET_KEY }}"
########## END SECRET CONFIGURATION

########## SESSION COOKIE
# See: https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = 'sessionid'
######### END SESSION COOKIE


# Set these to the correct values for your OAuth2/OpenID Connect provider (e.g., devstack)
SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ INSIGHTS_OAUTH2_KEY }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ INSIGHTS_OAUTH2_SECRET }}"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "http://lms:8000"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = "http://lms:8000/logout"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://{{ LMS_HOST }}:8000"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ INSIGHTS_BACKEND_OAUTH2_KEY }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ INSIGHTS_BACKEND_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

COURSE_API_URL = 'http://lms:8000/api/courses/v1/'
GRADING_POLICY_API_URL = 'http://lms:8000/api/grades/v1/'

MODULE_PREVIEW_URL = 'http://lms:8000/xblock'