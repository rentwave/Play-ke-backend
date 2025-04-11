#!/bin/bash

python manage.py collectstatic --no-input
PORT=8001
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --access-logfile - \
    --timeout 300 \
    dime_loans.wsgi:application -w 2
