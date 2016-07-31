@echo off
cd %~dp0

fab -f deploy_blog.py deploy

pause
