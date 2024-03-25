#!/bin/bash

# Start the first Python script in the background and get its PID
python src/serve_chatbot.py --server_port 5000 &
PID1=$!

# Start the second Python script in the background and get its PID
python src/app.py --host 127.0.0.1 --port 5001 --debug &
PID2=$!

# Function to kill the background jobs if this script is terminated
cleanup() {
    echo "Cleaning up..."
    kill $PID1 $PID2
    exit 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM signals and call cleanup function
trap cleanup SIGINT SIGTERM

# Wait for both background processes to finish
wait $PID1
wait $PID2