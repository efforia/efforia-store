#!/bin/sh
python manage.py collectstatic --noinput 
# Verify if the database exists on Postgres
if !(psql -U postgres -h db -lqt | cut -d \| -f 1 | grep -qw efforia); then
	psql -U postgres -h db -c "create database efforia;" 
fi
python manage.py makemigrations --settings="store.production"
python manage.py migrate --settings="store.production" 
gunicorn store.wsgi -b 0.0.0.0:9000
