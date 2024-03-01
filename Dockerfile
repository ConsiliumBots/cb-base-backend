FROM python:3.8
#REQs
ARG INPUT_ENVIRONMENT=dev
ENV ENVIRONMENT $INPUT_ENVIRONMENT
ENV DJANGO_SETTINGS_MODULE "config.settings.$ENVIRONMENT"


#LO DEMAS
RUN apt-get update --fix-missing
RUN apt-get upgrade -y
RUN apt-get -y install memcached libmemcached-tools libmemcached-dev zlib1g-dev gdal-bin vim systemctl gettext

# setup environment variable
ENV DockerHOME=/home/app/webapp

# set work directory
RUN mkdir -p /var/log/backend
RUN mkdir -p $DockerHOME


# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# install dependencies
COPY . $DockerHOME
#Extraccion secrets y paso a archivo de configuracion
RUN --mount=type=secret,id=mysecret cp /run/secrets/mysecret config/settings/secrets.json
RUN echo "Environment setted $ENVIRONMENT"
# run this command to install all dependencies

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system

# port where the Django app runs. It should be the same as the k8 deployment container httpGet.
EXPOSE 8000

RUN echo "Starting uWSGI"
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
