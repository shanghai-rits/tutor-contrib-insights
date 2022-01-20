FROM docker.io/ubuntu:20.04 as openedx

RUN apt update && \
  apt-get install -y software-properties-common && \
  apt-add-repository -y ppa:deadsnakes/ppa && apt-get update && \
  apt-get install -y curl && \
  apt-get upgrade -qy && \
  apt install -y git-core language-pack-en build-essential python3.8-dev python3.8-venv python3.8-distutils libmysqlclient-dev && \
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
  python3.8 get-pip.py && python3.8 -m pip install --upgrade pip setuptools && \
  rm -rf /var/lib/apt/lists/*

# Create python venv
RUN mkdir /openedx/ && python3.8 -m venv /openedx/venv/
ENV PATH "/openedx/venv/bin:$PATH"

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install insights
ARG INSIGHTS_REPOSITORY="https://github.com/edx/edx-analytics-dashboard.git"
# ARG INSIGHTS_VERSION={{ OPENEDX_COMMON_VERSION }}
ARG INSIGHTS_VERSION="master"
RUN mkdir -p /openedx/analytics_dashboard && \
    git clone $INSIGHTS_REPOSITORY --branch $INSIGHTS_VERSION --depth 1 /openedx/analytics_dashboard
WORKDIR /openedx/analytics_dashboard

WORKDIR /openedx/analytics_dashboard
RUN pip install -r requirements/production.txt
RUN pip install django-redis==4.12.1
# RUN pip install uwsgi==2.0.19.1

# Install private requirements: this is useful for installing custom payment processors.
COPY ./requirements/ /openedx/requirements
RUN cd /openedx/requirements/ \
  && touch ./private.txt \
  && pip install -r ./private.txt

# Setup minimal yml config file, which is required by production settings
RUN mkdir /openedx/settings/
RUN echo "{}" > /openedx/settings/insights.yml
ENV ANALYTICS_DASHBOARD_CFG /openedx/settings/insights.yml

# Install a recent version of nodejs
RUN pip install nodeenv
RUN nodeenv /openedx/nodeenv --node=12.13.0 --prebuilt
ENV PATH /openedx/nodeenv/bin:${PATH}

# Run the set up code 
RUN npm install 
RUN ./npm-post-install.sh
RUN make migrate
RUN make static

EXPOSE 18110
CMD gunicorn -b 0.0.0.0:18110 --workers 2 --timeout=300 analytics_dashboard.wsgi:application
# CMD uwsgi \
#     --static-map /static=/openedx/analytics_dashboard/analytics_dashboard/static \
#     --static-map /media=/openedx/analytics_dashboard/media \
#     --http 0.0.0.0:18110 \
#     --thunder-lock \
#     --single-interpreter \
#     --enable-threads \
#     --processes=2 \
#     --buffer-size=8192 \
#     --wsgi-file /openedx/analytics_dashboard/analytics_dashboard/wsgi.py

# RUN useradd -m --shell /bin/false app
# USER app
# COPY . /openedx/analytics_dashboard

FROM openedx as edx.org
RUN python3.8 -m pip install newrelic
CMD newrelic-admin run-program gunicorn -b 0.0.0.0:18110 --workers 2 --timeout=300 analytics_dashboard.wsgi:application