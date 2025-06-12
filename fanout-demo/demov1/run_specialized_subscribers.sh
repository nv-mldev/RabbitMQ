#!/bin/bash

# Script to run specialized subscribers for different services

echo "Starting specialized subscriber services..."

# Run each specialized subscriber in background
python notification_subscriber.py &
NOTIFICATION_PID=$!
echo "📧 Started Notification Service (PID: $NOTIFICATION_PID)"

python logging_subscriber.py &
LOGGING_PID=$!
echo "📝 Started Logging Service (PID: $LOGGING_PID)"

python analytics_subscriber.py &
ANALYTICS_PID=$!
echo "📊 Started Analytics Service (PID: $ANALYTICS_PID)"

python backup_subscriber.py &
BACKUP_PID=$!
echo "💾 Started Backup Service (PID: $BACKUP_PID)"

echo ""
echo "All services started successfully!"
echo "Each service will process the relevant part of incoming messages."
echo "Press Ctrl+C to stop all services."

# Function to clean up background processes
cleanup() {
    echo ""
    echo "Stopping all services..."
    kill $NOTIFICATION_PID $LOGGING_PID $ANALYTICS_PID $BACKUP_PID 2>/dev/null
    wait
    echo "All services stopped."
    exit 0
}

# Set up signal handler
trap cleanup SIGINT

# Wait for all background processes
wait
