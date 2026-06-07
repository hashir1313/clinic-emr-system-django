#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Pulling latest changes from GitHub..."
git pull

echo "Starting the Django development server on 0.0.0.0:8000..."
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!

sleep 2

echo "Opening http://localhost:8000/ in your browser..."
xdg-open http://localhost:8000/

wait $SERVER_PID
