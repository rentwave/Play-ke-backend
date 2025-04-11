#!/bin/bash

python manage.py collectstatic --no-input
PORT=8015
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --access-logfile - \
    --timeout 300 \
    playke.wsgi:application -w 2
