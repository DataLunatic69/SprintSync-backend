#!/bin/bash
set -e

echo "Setting up database connection for Alembic..."
export SQLALCHEMY_URL=$DATABASE_URL

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT