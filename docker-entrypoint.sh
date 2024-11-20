#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
python manage.py migrate --noinput
python manage.py createcachetable
exec gunicorn sca.wsgi:application -c "${APP_DIR}/gunicorn.conf.py"
