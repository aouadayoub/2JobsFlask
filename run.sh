#!/bin/bash

# Wait for a few seconds to ensure services like MongoDB and Redis are available
echo "Waiting for MongoDB and Redis to be available..."
sleep 4

# Start the Flask app with Gunicorn
echo "Starting Flask app with Gunicorn..."
gunicorn app:app --bind 0.0.0.0:${PORT} --workers 4
