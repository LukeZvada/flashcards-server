#!/bin/bash
rm -rf flashcardsapi/migrations
rm db.sqlite3
python manage.py makemigrations flashcardsapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata questionsBE1a
python manage.py loaddata questionsBE1b
python manage.py loaddata questionsBE2
python manage.py loaddata questionsBE3
python manage.py loaddata questionsFE1
python manage.py loaddata questionsFE2
python manage.py loaddata questionsFE3
python manage.py loaddata questionsFE4