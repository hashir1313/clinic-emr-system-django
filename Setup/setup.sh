#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "=== Clinic EMR System Setup ==="
echo ""

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r ../requirements.txt

echo "Running database migrations..."
python ../manage.py migrate

echo ""
echo "Creating admin account..."
python ../manage.py createsuperuser

echo ""
echo "=== Setup complete! ==="
echo "Run ./start.sh to launch the application."
