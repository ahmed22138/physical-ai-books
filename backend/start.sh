#!/bin/bash
# Start script for Render deployment

echo "Starting Physical AI Textbook Backend..."
echo "Environment: $ENVIRONMENT"
echo "Python version: $(python --version)"

# Run database migrations if needed (optional)
# alembic upgrade head

# Start the FastAPI server
exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
