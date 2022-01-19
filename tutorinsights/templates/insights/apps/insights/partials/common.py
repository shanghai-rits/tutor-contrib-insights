import os
from os.path import abspath, basename, dirname, join, normpath
# from sys import path

next_page='/'"""Common settings and globals."""


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Your Name', 'your_email@example.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ INSIGHTS_DASHBOARD_MYSQL_DATABASE }}',
        'USER': '{{ INSIGHTS_MYSQL_USER }}',
        'PASSWORD': '{{ INSIGHTS_MYSQL_PASSWORD }}',
        'HOST': '{{ MYSQL_HOST }}',
        'PORT': '{{ MYSQL_PORT }}',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
########## END DATABASE CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = '{{ INSIGHTS_SECRET_KEY }}'
########## END SECRET CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "{{ INSIGHTS_HOST }}",
    "insights",
]
########## END SITE CONFIGURATION

########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#middleware-classes
MIDDLEWARE = [
    'edx_django_utils.monitoring.DeploymentMonitoringMiddleware',
    'edx_django_utils.cache.middleware.RequestCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'core.middleware.LanguagePreferenceMiddleware',
    'core.middleware.ServiceUnavailableExceptionMiddleware',
    'courses.middleware.CourseMiddleware',
    'courses.middleware.CoursePermissionsExceptionMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'help.middleware.HelpURLMiddleware',
    'edx_django_utils.cache.middleware.TieredCacheMiddleware',
    'edx_rest_framework_extensions.middleware.RequestMetricsMiddleware',
]
########## END MIDDLEWARE CONFIGURATION


# Apps specific for this project go here.
LOCAL_APPS = (
    'analytics_dashboard.core',
    'analytics_dashboard.courses',
    'analytics_dashboard.help',
    'soapbox',
)

THIRD_PARTY_APPS = (
    'release_util',
    'rest_framework',
    'social_django',
    'webpack_loader'
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION

LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": "/var/log/ecommerce.log",
    "formatter": "standard",
}
########## END LOGGING CONFIGURATION

########## SUPPORT -- Ths value should be overridden for production deployments.
SUPPORT_EMAIL = 'support@example.com'
HELP_URL = 'http://127.0.0.1/en/latest'
TERMS_OF_SERVICE_URL = 'http://example.com/terms-service'
########## END FEEDBACK

########## EMAIL CONFIG
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "{{ SMTP_HOST }}"
EMAIL_PORT = "{{ SMTP_PORT }}"
EMAIL_HOST_USER = "{{ SMTP_USERNAME }}"
EMAIL_HOST_PASSWORD = "{{ SMTP_PASSWORD }}"
EMAIL_USE_TLS = "{{ SMTP_USE_TLS }}"
########## END EMAIL CONFIG

########## LANDING PAGE -- URLs should be overridden for production deployments.
SHOW_LANDING_RESEARCH = True
RESEARCH_URL = 'https://www.edx.org/research-pedagogy'
OPEN_SOURCE_URL = 'http://example.com/'
########## END LANDING PAGE

########## DOCUMENTATION LINKS -- These values should be overridden for production deployments.
DOCUMENTATION_LOAD_ERROR_URL = 'http://127.0.0.1/en/latest/Reference.html#error-conditions'
# evaluated again at the end of production setting after DOCUMENTATION_LOAD_ERROR_URL has been set
DOCUMENTATION_LOAD_ERROR_MESSAGE = f'<a href="{DOCUMENTATION_LOAD_ERROR_URL}" target="_blank">Read more</a>.'
########## END DOCUMENTATION LINKS


########## DATA API CONFIGURATION
DATA_API_URL = 'http://{{ INSIGHTS_ANALYTICSAPI_HOST }}/api/v0'
DATA_API_AUTH_TOKEN = '{{ INSIGHTS_API_AUTH_TOKEN }}'
########## END DATA API CONFIGURATION

# used to determine if a course ID is valid
LMS_COURSE_VALIDATION_BASE_URL = None

# used to construct the shortcut link to course modules
LMS_COURSE_SHORTCUT_BASE_URL = 'http://{ LMS_HOST }/courses'

# used to construct the shortcut link to view/edit a course in Studio
CMS_COURSE_SHORTCUT_BASE_URL = 'http://{{ CMS_HOST }}/courses/'

# Used to determine how dates and time are displayed in templates
# The strings are intended for use with the django.utils.dateformat
# module, which uses the PHP's date() style. Format details are
# described at http://www.php.net/date.
DATE_FORMAT = 'F d, Y'
TIME_FORMAT = 'g:i A'

########## AUTHENTICATION
AUTH_USER_MODEL = 'core.User'

# Allow authentication via edX OAuth2
AUTHENTICATION_BACKENDS = (
    'auth_backends.backends.EdXOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Set to true if using SSL and running behind a proxy
SOCIAL_AUTH_REDIRECT_IS_HTTPS = {% if ENABLE_HTTPS %}True{% else %}False{% endif %}

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email']

SOCIAL_AUTH_STRATEGY = 'auth_backends.strategies.EdxDjangoStrategy'

# Set these to the correct values for your OAuth2 provider (e.g., devstack)
SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ INSIGHTS_OAUTH2_KEY }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ INSIGHTS_OAUTH2_SECRET }}"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "http://lms:8000"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = "http://lms:8000/logout"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ INSIGHTS_BACKEND_OAUTH2_KEY }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ INSIGHTS_BACKEND_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/courses/'
LOGOUT_REDIRECT_URL = '/'

# Determines if course permissions should be checked before rendering course views.
ENABLE_COURSE_PERMISSIONS = True

########## END AUTHENTICATION

# The application and platform display names to be used in templates, emails, etc.
PLATFORM_NAME = '{{ PLATFORM_NAME }}'
APPLICATION_NAME = 'Insights'
FULL_APPLICATION_NAME = f'{PLATFORM_NAME} {APPLICATION_NAME}'

########## COURSE API
COURSE_API_URL = 'http://lms:8000/api/courses/v1/'
GRADING_POLICY_API_URL = 'http://lms:8000/api/grades/v1/'

# If no key is specified, the authenticated user's OAuth2 access token will be used.
COURSE_API_KEY = None
########## END COURSE API

########## MODULE_PREVIEW
MODULE_PREVIEW_URL = 'http://{{ LMS_HOST }}/xblock'
########## END MODULE_PREVIEW

########## EXTERNAL SERVICE TIMEOUTS
# Time in seconds that Insights should wait on external services
# before giving up.  These values should be overridden in
# configuration.
ANALYTICS_API_DEFAULT_TIMEOUT = 10
LMS_DEFAULT_TIMEOUT = 5
########## END EXTERNAL SERVICE TIMEOUTS

_ = lambda s: s

FOOTER_LINKS = (
    {'url': 'http://example.com/', 'text': _('Terms of Service'), 'data_role': 'tos'},
    {'url': 'http://example.com/', 'text': _('Privacy Policy'), 'data_role': 'privacy-policy'},
)


########## COURSE_ID_PATTERN
# Regex used to capture course_ids from URLs
COURSE_ID_PATTERN = r'(?P<course_id>[^/+]+[/+][^/+]+[/+][^/]+)'
########## END COURSE_ID_PATTERN

########## LEARNER_API_LIST_DOWNLOAD_FIELDS
# Comma-delimited list of field names to include in the Learner List CSV download
# e.g., # "username,segments,cohort,engagements.videos_viewed,last_updated"
# Default (None) includes all available fields, in alphabetical order.
LEARNER_API_LIST_DOWNLOAD_FIELDS = None
########## END LEARNER_API_LIST_DOWNLOAD_FIELDS

########## BLOCK_LEARNER_ANALYTICS_ORG_LIST
BLOCK_LEARNER_ANALYTICS_ORG_LIST = []
########## END BLOCK_LEARNER_ANALYTICS_ORG_LIST

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "KEY_PREFIX": "insights",
        "LOCATION": "redis://{% if REDIS_USERNAME and REDIS_PASSWORD %}{{ REDIS_USERNAME }}:{{ REDIS_PASSWORD }}{% endif %}@{{ REDIS_HOST }}:{{ REDIS_PORT }}/{{ INSIGHTS_CACHE_REDIS_DB }}",
    }
}
COURSE_SUMMARIES_CACHE_TIMEOUT = 3600  # 1 hour timeout
########## END CACHE CONFIGURATION

########## WEBPACK CONFIGURATION
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(SITE_ROOT, 'webpack-stats.json'),
    }
}
########## END WEBPACK CONFIGURATION

########## CDN CONFIGURATION
CDN_DOMAIN = None  # production will not use a CDN for static assets if this is set to a falsy value
########## END CDN CONFIGURATION

########## LANGUAGE COOKIE
# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-cookie-name
LANGUAGE_COOKIE_NAME = 'insights_language'
########## END LANGUAGE COOKIE

########## CSRF COOKIE
# See: https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = 'insights_csrftoken'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
# CSRF_COOKIE_SECURE = False
######### END CSRF COOKIE

########## SESSION COOKIE
# See: https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = 'insights_sessionid'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#session-expire-at-browser-close
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
######### END SESSION COOKIE

COURSE_SUMMARIES_IDS_CUTOFF = 500

PRIVACY_POLICY_URL = 'http://{{ INSIGHTS_HOST }}/privacy-policy'

CORS_ALLOW_CREDENTIALS = True

import json

{% set jwt_rsa_key = rsa_import_key(JWT_RSA_PRIVATE_KEY) %}
JWT_AUTH["JWT_ISSUER"] = "{{ JWT_COMMON_ISSUER }}"
JWT_AUTH["JWT_AUDIENCE"] = "{{ JWT_COMMON_AUDIENCE }}"
JWT_AUTH["JWT_SECRET_KEY"] = "{{ JWT_COMMON_SECRET_KEY }}"
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "{{ jwt_rsa_key.e|long_to_base64 }}",
                "n": "{{ jwt_rsa_key.n|long_to_base64 }}",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "{{ JWT_COMMON_ISSUER }}",
        "AUDIENCE": "{{ JWT_COMMON_AUDIENCE }}",
        "SECRET_KEY": "{{ OPENEDX_SECRET_KEY }}"
    }
]

ENTERPRISE_SERVICE_URL = '{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/enterprise/'
ENTERPRISE_API_URL = ENTERPRISE_SERVICE_URL + 'api/v1/'