#!/bin/bash
#export LANG=en_US.UTF-8
echo "DJANGO_SETTINGS_MODULE-->$DJANGO_SETTINGS_MODULE"
python3 manage.py migrate --settings=$DJANGO_SETTINGS_MODULE
python3 manage.py compilemessages
python3 manage.py collectstatic --clear --noinput --settings=$DJANGO_SETTINGS_MODULE
python3 manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS_MODULE
# Start uWSGI processes
if [[ -z "$ENVIRONMENT" || "$ENVIRONMENT" = "dev" ]]; then
  echo "Using Default Settings"
  export UWSGI_FILE=uwsgi_v2.ini
else
  if [[ "$ENVIRONMENT" = "staging" || "$ENVIRONMENT" = "production" ]]; then
      echo "Using Cloud Settings"
      export UWSGI_FILE=config/uwsgi_v2.cloud.ini
  fi
fi
exec uwsgi --http 0.0.0.0:8000 --module config.wsgi --ini $UWSGI_FILE
