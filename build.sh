#!/bin/sh

pip install -r requirements.txt  # Add this line
python manage.py migrate
python manage.py collectstatic --noinput
