FROM docker.io/ubuntu:20.04 as app

RUN apt update && \
  apt-get install -y software-properties-common && \
  apt-add-repository -y ppa:deadsnakes/ppa && apt-get update && \
  apt install -y git-core language-pack-en python3.8-dev python3.8-venv libmysqlclient-dev libffi-dev libssl-dev build-essential gettext openjdk-8-jdk && \
  rm -rf /var/lib/apt/lists/*

# Create python venv
RUN mkdir /openedx/ && python3.8 -m venv /openedx/venv/
ENV PATH "/openedx/venv/bin:$PATH"

RUN pip install pip==20.2.3 setuptools==50.3.0

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
# ENV ANALYTICS_API_CFG /edx/etc/analytics_api.yml

# Install analytics api
ARG ANALYTICSAPI_REPOSITORY="https://github.com/edx/edx-analytics-data-api"
# ARG ANALYTICSAPI_VERSION={{ OPENEDX_COMMON_VERSION }}
ARG ANALYTICSAPI_VERSION="master"
RUN mkdir -p /openedx/analytics_api && \
    git clone $ANALYTICSAPI_REPOSITORY --branch $ANALYTICSAPI_VERSION --depth 1 /openedx/analytics_api
WORKDIR /openedx/analytics_api

WORKDIR /openedx/analytics_api
COPY requirements /openedx/analytics_api/requirements
RUN pip install -r requirements/production.txt

# Install private requirements: this is useful for installing custom payment processors.
COPY ./requirements/ /openedx/requirements
RUN cd /openedx/requirements/ \
  && touch ./private.txt \
  && pip install -r ./private.txt

# Setup minimal yml config file, which is required by production settings
RUN mkdir /openedx/settings/ 
RUN echo "{}" > /openedx/settings/insights.yml
ENV ANALYTICS_API_CFG /openedx/settings/insights.yml

COPY gunicorn/ /openedx/analytics_api/analytics_data_api/

EXPOSE 19001
CMD gunicorn --bind=0.0.0.0:19001 --workers 2 --max-requests=1000 -c /openedx/analytics_api/analytics_data_api/docker_gunicorn_configuration.py analyticsdataserver.wsgi:application

# RUN useradd -m --shell /bin/false app
# USER app


FROM app as newrelic
RUN pip install newrelic
CMD newrelic-admin run-program gunicorn --bind=0.0.0.0:19001 --workers 2 --max-requests=1000 -c /openedx/analytics_api/analytics_data_api/docker_gunicorn_configuration.py analyticsdataserver.wsgi:application
