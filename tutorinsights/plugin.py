from glob import glob
import os
import pkg_resources

from .__about__ import __version__

templates = pkg_resources.resource_filename(
    "tutorinsights", "templates"
)

config = {
    "add": {
        "INSIGHTS_MYSQL_PASSWORD": "{{ 8|random_string }}",
        "API_AUTH_TOKEN": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "INSIGHTS_OAUTH2_SECRET": "{{ 8|random_string }}",
        "ANALYTICSAPI_OAUTH2_SECRET": "{{ 8|random_string }}",
        "INSIGHTS_BACKEND_OAUTH2_SECRET": "{{ 8|random_string }}",
        "ANALYTICSAPI_BACKEND_OAUTH2_SECRET": "{{ 8|random_string }}",
        "SEGMENT_WRITE_KEY": "{{ 20|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "INSIGHTS_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}edxops/insights:latest",
        "ANALYTICSAPI_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}edxops/analytics_api:latest",
        "INSIGHTS_HOST": "insights.{{ LMS_HOST }}",
        "ANALYTICSAPI_HOST": "analyticsapi.{{ LMS_HOST }}",
        "INDEX_OVERRIDES": {},
        "DASHBOARD_MYSQL_DATABASE": "dashboard",
        "ANALYTICSAPI_MYSQL_DATABASE": "analytics-api",
        "REPORTS_MYSQL_DATABASE": "reports",
        "INSIGHTS_MYSQL_USER": "analytics001",
        "ANALYTICSAPI_MYSQL_USER": "api001",
        "INSIGHTS_OAUTH2_KEY": "insights-sso-key",
        "INSIGHTS_BACKEND_OAUTH2_KEY": "insights-backend-service-key",
        "ANALYTICSAPI_OAUTH2_KEY": "analytics_api-sso-key",
        "ANALYTICSAPI_BACKEND_OAUTH2_KEY": "analytics_api-backend-service-key",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
        "INSIGHTS_ELASTICSEARCH_INDEX": "learner",
        "INSIGHTS_ELASTICSEARCH_UPDATE_INDEX": "index_update",
        "ANALYTICSAPI_COURSE_BLOCK_API": "",
    },
}

hooks = {
    "init": ["mysql", "lms", "analyticsapi", "insights"],
    "build-image": {
        "insights": "{{ INSIGHTS_DOCKER_IMAGE }}",
        "analyticsapi": "{{ ANALYTICS_API_DOCKER_IMAGE }}",
    },
    "remote-image": {
        "insights": "{{ INSIGHTS_DOCKER_IMAGE }}",
        "analyticsapi": "{{ ANALYTICS_API_DOCKER_IMAGE }}",
    },
}


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename(
        "tutorinsights", "patches"
    )
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
