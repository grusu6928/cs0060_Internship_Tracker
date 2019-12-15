#!/usr/bin/env bash
# starts up flask app

# generate APP_SECRET e.g. via APP_SECRET=`openssl rand -base64 32`
export APP_SECRET=`openssl rand -base64 32`
exec gunicorn -w 3 -b 0.0.0.0:5000 --access-logfile - --error-logfile - main:app
