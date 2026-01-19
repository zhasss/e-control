#!/usr/bin/env sh
set -e

echo "==> Migrating..."
python manage.py migrate --noinput

echo "==> Collectstatic..."
python manage.py collectstatic --noinput || true

echo "==> Starting server..."
exec gunicorn econtrol.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-3} \
  --timeout ${GUNICORN_TIMEOUT:-120}
