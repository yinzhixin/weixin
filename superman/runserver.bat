@echo off
cd %~dp0

python manage.py runserver 0.0.0.0:8000 --insecure
