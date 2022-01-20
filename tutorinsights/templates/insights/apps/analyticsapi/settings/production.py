"""Production settings and globals."""



from os import environ

import six
import yaml
# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

{% include "insights/apps/analyticsapi/settings/partials/common.py" %}
from analyticsdataserver.settings.logger import get_logger_config

LOGGING = get_logger_config()

def get_env_setting(setting):
    """Get the environment setting or return exception."""
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['*']
########## END HOST CONFIGURATION

CONFIG_FILE=get_env_setting('ANALYTICS_API_CFG')

with open(CONFIG_FILE) as f:
  config_from_yaml = yaml.load(f, Loader=yaml.FullLoader)

REPORT_DOWNLOAD_BACKEND = config_from_yaml.pop('REPORT_DOWNLOAD_BACKEND', {})

JWT_AUTH_CONFIG = config_from_yaml.pop('JWT_AUTH', {})
JWT_AUTH.update(JWT_AUTH_CONFIG)

vars().update(config_from_yaml)
vars().update(REPORT_DOWNLOAD_BACKEND)

### TODO: Add these inside the config.yml file
LMS_BASE_URL = '{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}'
########## EMAIL CONFIGURATION

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION

########## ELASTICSEARCH CONFIGURATION
ELASTICSEARCH_LEARNERS_HOST = "{{ ELASTICSEARCH_HOST }}"
ELASTICSEARCH_LEARNERS_INDEX = "{{ INSIGHTS_ELASTICSEARCH_INDEX }}"
ELASTICSEARCH_LEARNERS_INDEX_ALIAS = "{{ INSIGHTS_ELASTICSEARCH_INDEX_ALIAS }}"
ELASTICSEARCH_LEARNERS_UPDATE_INDEX = "{{ INSIGHTS_ELASTICSEARCH_UPDATE_INDEX }}"

# access credentials for signing requests to AWS.
# For more information see http://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html
ELASTICSEARCH_AWS_ACCESS_KEY_ID = None
ELASTICSEARCH_AWS_SECRET_ACCESS_KEY = None
# override the default elasticsearch connection class and useful for signing certificates
# e.g. 'analytics_data_api.v0.connections.BotoHttpConnection'
ELASTICSEARCH_CONNECTION_CLASS = None
# only needed with BotoHttpConnection, e.g. 'us-east-1'
ELASTICSEARCH_CONNECTION_DEFAULT_REGION = None

DEFAULT_ELASTICSEARCH_INDEX_SETTINGS = {
    'number_of_shards': 1,
    'number_of_replicas': 0
}
ELASTICSEARCH_INDEX_SETTINGS = environ.get('ELASTICSEARCH_INDEX_SETTINGS', DEFAULT_ELASTICSEARCH_INDEX_SETTINGS)
########## END ELASTICSEARCH CONFIGURATION

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

## config.yml END

DB_OVERRIDES = dict(
    PASSWORD=environ.get('DB_MIGRATION_PASS', DATABASES['default']['PASSWORD']),
    ENGINE=environ.get('DB_MIGRATION_ENGINE', DATABASES['default']['ENGINE']),
    USER=environ.get('DB_MIGRATION_USER', DATABASES['default']['USER']),
    NAME=environ.get('DB_MIGRATION_NAME', DATABASES['default']['NAME']),
    HOST=environ.get('DB_MIGRATION_HOST', DATABASES['default']['HOST']),
    PORT=environ.get('DB_MIGRATION_PORT', DATABASES['default']['PORT']),
)

for override, value in DB_OVERRIDES.items():
    DATABASES['default'][override] = value
