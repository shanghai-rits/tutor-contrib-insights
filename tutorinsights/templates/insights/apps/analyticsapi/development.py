"""Development settings and globals."""

from ..devstack import *

{% include "insights/apps/analyticsapi/settings/partials/common.py" %}


from os.path import join, normpath

from corsheaders.defaults import default_headers as corsheaders_default_headers

from analyticsdataserver.settings.base import *

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(DJANGO_ROOT, 'default.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'analytics': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(DJANGO_ROOT, 'analytics.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'analytics_v1': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(DJANGO_ROOT, 'analytics.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'enterprise': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(DJANGO_ROOT, 'enterprise_reporting.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }
########## END CACHE CONFIGURATION


########## ANALYTICS DATA API CONFIGURATION

ANALYTICS_DATABASE = 'analytics'
ENTERPRISE_REPORTING_DB_ALIAS = 'analytics'
ANALYTICS_DATABASE_V1 = 'analytics'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SWAGGER_SETTINGS = {
    'api_key': 'edx'
}

# These two settings are used in generate_fake_course_data.py.
# Replace with correct values to generate local fake video data.
LMS_BASE_URL = 'http://{{ LMS_HOST }}/'  # the base URL for your running local LMS instance
COURSE_BLOCK_API_AUTH_TOKEN = '{{ ANALYTICSAPI_COURSE_BLOCK_API }}'  # see README for instructions on how to configure this value

# In Insights, we run this API as a separate service called "analyticsapi" to run acceptance/integration tests. Docker
# saves the service name as a host in the Insights container so it can reach the API by requesting http://analyticsapi/.
# However, in Django 1.10.3, the HTTP_HOST header of requests started to be checked against the ALLOWED_HOSTS setting
# even in DEBUG=True mode. Here, we add the Docker service name "analyticsapi" to the default set of local allowed
# hosts.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1', 'analyticsapi', 'host.docker.internal', "{{ ANALYTICSAPI_HOST }}"]

JWT_AUTH.update({
    'JWT_SECRET_KEY': 'lms-secret',
    'JWT_ISSUER': 'http://lms:8000/oauth2',
    'JWT_AUDIENCE': None,
    'JWT_VERIFY_AUDIENCE': False,
    'JWT_PUBLIC_SIGNING_JWK_SET': (
        '{"keys": [{"kid": "devstack_key", "e": "AQAB", "kty": "RSA", "n": "smKFSYowG6nNUAdeqH1jQQnH1PmIHphzBmwJ5vRf1vu'
        '48BUI5VcVtUWIPqzRK_LDSlZYh9D0YFL0ZTxIrlb6Tn3Xz7pYvpIAeYuQv3_H5p8tbz7Fb8r63c1828wXPITVTv8f7oxx5W3lFFgpFAyYMmROC'
        '4Ee9qG5T38LFe8_oAuFCEntimWxN9F3P-FJQy43TL7wG54WodgiM0EgzkeLr5K6cDnyckWjTuZbWI-4ffcTgTZsL_Kq1owa_J2ngEfxMCObnzG'
        'y5ZLcTUomo4rZLjghVpq6KZxfS6I1Vz79ZsMVUWEdXOYePCKKsrQG20ogQEkmTf9FT_SouC6jPcHLXw"}]}'
    ),
})

CORS_ORIGIN_WHITELIST = (
    'http://localhost:1991',
)
CORS_ALLOW_HEADERS = corsheaders_default_headers + (
    'use-jwt-cookie',
)
CORS_ALLOW_CREDENTIALS = True

# Default elasticsearch port when running locally
ELASTICSEARCH_LEARNERS_HOST = "{{ ELASTICSEARCH_HOST }}"
ELASTICSEARCH_LEARNERS_INDEX = 'roster_entry_001'
ELASTICSEARCH_LEARNERS_INDEX_ALIAS = 'roster_entry'
ELASTICSEARCH_LEARNERS_UPDATE_INDEX = 'index_update'

########## END ANALYTICS DATA API CONFIGURATION

"""Devstack settings."""


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ ANALYTICSAPI_MYSQL_DATABASE }}',
        'USER': '{{ ANALYTICSAPI_MYSQL_USER }}',
        'PASSWORD': '{{ INSIGHTS_MYSQL_PASSWORD }}',
        'HOST': '{{ MYSQL_HOST }}',
        'PORT': '{{ MYSQL_PORT }}',
    },
    # 'analytics_v1': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'reports_v1',
    #     'USER': '{{ ANALYTICSAPI_MYSQL_USER }}',
    #     'PASSWORD': '{{ INSIGHTS_MYSQL_PASSWORD }}',
    #     'HOST': '{{  }}',
    #     'PORT': '3306',
    # },
    'analytics': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ REPORTS_MYSQL_DATABASE }}',
        'USER': '{{ ANALYTICSAPI_MYSQL_USER }}',
        'PASSWORD': '{{ INSIGHTS_MYSQL_PASSWORD }}',
        'HOST': '{{ MYSQL_HOST }}',
        'PORT': '{{ MYSQL_PORT }}',
    }
}

# DB_OVERRIDES = dict(
#     USER=os.environ.get('DB_USER', DATABASES['default']['USER']),
#     PASSWORD=os.environ.get('DB_PASSWORD', DATABASES['default']['PASSWORD']),
#     HOST=os.environ.get('DB_HOST', DATABASES['default']['HOST']),
#     PORT=os.environ.get('DB_PORT', DATABASES['default']['PORT']),
# )

# for override, value in DB_OVERRIDES.items():
#     DATABASES['default'][override] = value
#     DATABASES['analytics'][override] = value
#     DATABASES['analytics_v1'][override] = value
########## END DATABASE CONFIGURATION

# ELASTICSEARCH_LEARNERS_HOST = os.environ.get('ELASTICSEARCH_LEARNERS_HOST', 'edx.devstack.elasticsearch')

# ALLOWED_HOSTS += ['{{edx.devstack.analyticsapi}}']

LMS_BASE_URL = "http://{{ LMS_HOST }}"
