#!/bin/bash

# Script to run multiple subscriber instances in parallel

echo "Starting the publisher..."
# Run the publisher in background
python publisher.py &
PUBLISHER_PID=$!
echo "Started publisher (PID: $PUBLISHER_PID)"

echo "Starting multiple subscribers..."

# Run subscribers in background
python subscriber.py &
echo "Started subscriber 1 (PID: $!)"

python subscriber.py &
echo "Started subscriber 2 (PID: $!)"

python subscriber.py &
echo "Started subscriber 3 (PID: $!)"

python subscriber.py &
echo "Started subscriber 4 (PID: $!)"

echo "All subscribers started. Press Ctrl+C to stop all."

# Wait for all background processes
wait
