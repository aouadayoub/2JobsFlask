#!/bin/bash

# Start MongoDB
echo "Starting MongoDB..."
mongod &

# Start Redis
echo "Starting Redis..."
redis-server &

# Wait for 4 seconds
echo "Waiting for MongoDB and Redis to start..."
sleep 4

# Start Flask App
echo "Starting Flask App..."
python app.py & 

# Keep the script running in the foreground
wait -n 