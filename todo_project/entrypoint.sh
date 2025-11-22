#!/bin/sh
set -e

# Wait for DB migrations and then run the server. The SQLITE_FILE env var
# should point at a file inside a host-mounted directory (e.g. /data/db.sqlite3)

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Django development server on 0.0.0.0:8000"
exec python manage.py runserver 0.0.0.0:8000
