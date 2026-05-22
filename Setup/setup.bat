@echo off
cd /d "%~dp0"

echo === Clinic EMR System Setup ===
echo.

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Running database migrations...
python manage.py migrate

echo.
echo Creating admin account...
python manage.py createsuperuser

echo.
echo === Setup complete! ===
echo Run start.bat to launch the application.
pause
