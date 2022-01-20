from glob import glob
import os
import pkg_resources

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "API_AUTH_TOKEN": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_DEV": "{{ 8|random_string }}",
        "ANALYTICSAPI_OAUTH2_SECRET": "{{ 8|random_string }}",
        "BACKEND_OAUTH2_SECRET": "{{ 8|random_string }}",
        "ANALYTICSAPI_BACKEND_OAUTH2_SECRET": "{{ 8|random_string }}",
        "SEGMENT_WRITE_KEY": "{{ 20|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "tutorcontribinsights-insights:latest",
        "ANALYTICSAPI_DOCKER_IMAGE": "tutorcontribinsights-api:latest",
        "HOST": "insights.{{ LMS_HOST }}",
        "ANALYTICSAPI_HOST": "analyticsapi.{{ LMS_HOST }}",
        "INDEX_OVERRIDES": {},
        "DASHBOARD_MYSQL_DATABASE": "dashboard",
        "ANALYTICSAPI_MYSQL_DATABASE": "analytics_api",
        "REPORTS_MYSQL_DATABASE": "reports",
        "MYSQL_USER": "analytics001",
        "ANALYTICSAPI_MYSQL_USER": "api001",
        "OAUTH2_KEY": "insights-sso-key",
        "OAUTH2_KEY_DEV": "insights-sso-key-dev",
        "BACKEND_OAUTH2_KEY": "insights-backend-service-key",
        "ANALYTICSAPI_OAUTH2_KEY": "analytics_api-sso-key",
        "ANALYTICSAPI_BACKEND_OAUTH2_KEY": "analytics_api-backend-service-key",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
        "ELASTICSEARCH_INDEX": "learner",
        "ELASTICSEARCH_UPDATE_INDEX": "index_update",
        "ANALYTICSAPI_COURSE_BLOCK_API": "",
    },
}

hooks = {
    "build-image": {
        "insights": "{{ INSIGHTS_DOCKER_IMAGE }}",
        "analyticsapi": "{{ INSIGHTS_ANALYTICS_API_DOCKER_IMAGE }}",
    },
    "remote-image": {
        "insights": "{{ INSIGHTS_DOCKER_IMAGE }}",
        "analyticsapi": "{{ INSIGHTS_ANALYTICS_API_DOCKER_IMAGE }}",
    },
    "init": ["mysql", "lms", "analyticsapi", "insights"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches