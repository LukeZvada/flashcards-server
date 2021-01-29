#!/bin/bash
rm -rf flashcardsapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations flashcardsapi
python manage.py migrate flashcardsapi