@echo off
cd /d "%~dp0"

echo Pulling latest changes from GitHub...
git pull

echo Starting the Django development server...
call venv\Scripts\activate
start /B python manage.py runserver

timeout /t 2 /nobreak >nul

echo Opening http://localhost:8000/ in your browser...
start http://localhost:8000/

pause
