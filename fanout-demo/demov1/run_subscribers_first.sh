#!/bin/bash

# Script to run multiple subscriber instances in parallel
# Starts subscribers first to ensure they don't miss messages

echo "Starting multiple subscribers first..."

# Start subscribers in background
python3 subscriber.py &
SUB1_PID=$!
echo "Started subscriber 1 (PID: $SUB1_PID)"

python3 subscriber.py &
SUB2_PID=$!
echo "Started subscriber 2 (PID: $SUB2_PID)"

python3 subscriber.py &
SUB3_PID=$!
echo "Started subscriber 3 (PID: $SUB3_PID)"

python3 subscriber.py &
SUB4_PID=$!
echo "Started subscriber 4 (PID: $SUB4_PID)"

# Give subscribers time to connect and create queues
echo "Waiting 2 seconds for subscribers to initialize..."
sleep 2

echo "Starting the publisher..."
python3 publisher.py &
PUBLISHER_PID=$!
echo "Started publisher (PID: $PUBLISHER_PID)"

echo ""
echo "All services started successfully!"
echo "Subscribers: $SUB1_PID, $SUB2_PID, $SUB3_PID, $SUB4_PID"
echo "Publisher: $PUBLISHER_PID"
echo "Press Ctrl+C to stop all."

# Function to clean up background processes
cleanup() {
    echo ""
    echo "Stopping all processes..."
    kill $SUB1_PID $SUB2_PID $SUB3_PID $SUB4_PID $PUBLISHER_PID 2>/dev/null
    wait
    echo "All processes stopped."
    exit 0
}

# Set up signal handler
trap cleanup SIGINT

# Wait for all background processes
wait
