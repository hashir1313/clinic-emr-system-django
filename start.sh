#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn clinic_emr.wsgi --bind 0.0.0.0:$PORT
