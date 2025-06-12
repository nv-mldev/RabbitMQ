#!/bin/bash

# Enhanced script with better output visibility
# Subscribers output to separate log files for clarity

echo "🚀 Starting multiple subscribers with visible output..."

# Create logs directory if it doesn't exist
mkdir -p logs

# Start subscribers in background with output redirected to files
echo "📝 Starting subscriber 1..."
python subscriber.py > logs/subscriber1.log 2>&1 &
SUB1_PID=$!
echo "   → Subscriber 1 (PID: $SUB1_PID) - Output: logs/subscriber1.log"

echo "📝 Starting subscriber 2..."
python subscriber.py > logs/subscriber2.log 2>&1 &
SUB2_PID=$!
echo "   → Subscriber 2 (PID: $SUB2_PID) - Output: logs/subscriber2.log"

echo "📝 Starting subscriber 3..."
python subscriber.py > logs/subscriber3.log 2>&1 &
SUB3_PID=$!
echo "   → Subscriber 3 (PID: $SUB3_PID) - Output: logs/subscriber3.log"

echo "📝 Starting subscriber 4..."
python subscriber.py > logs/subscriber4.log 2>&1 &
SUB4_PID=$!
echo "   → Subscriber 4 (PID: $SUB4_PID) - Output: logs/subscriber4.log"

# Give subscribers time to connect
echo ""
echo "⏳ Waiting 3 seconds for subscribers to initialize..."
sleep 3

echo ""
echo "📤 Starting publisher..."
python publisher.py
echo "✅ Publisher finished sending messages"

echo ""
echo "📊 Subscriber outputs:"
echo "=================================="

# Show the output from each subscriber
echo ""
echo "🔍 Subscriber 1 received:"
cat logs/subscriber1.log | grep "Received:" || echo "   (No messages yet)"

echo ""
echo "🔍 Subscriber 2 received:"
cat logs/subscriber2.log | grep "Received:" || echo "   (No messages yet)"

echo ""
echo "🔍 Subscriber 3 received:"
cat logs/subscriber3.log | grep "Received:" || echo "   (No messages yet)"

echo ""
echo "🔍 Subscriber 4 received:"
cat logs/subscriber4.log | grep "Received:" || echo "   (No messages yet)"

echo ""
echo "=================================="
echo "💡 To see live updates, run in another terminal:"
echo "   tail -f logs/subscriber*.log"
echo ""
echo "🛑 Press Ctrl+C to stop all subscribers"

# Function to clean up
cleanup() {
    echo ""
    echo "🔄 Stopping all subscribers..."
    kill $SUB1_PID $SUB2_PID $SUB3_PID $SUB4_PID 2>/dev/null
    wait
    echo "✅ All subscribers stopped"
    echo "📁 Log files saved in logs/ directory"
    exit 0
}

# Set up signal handler
trap cleanup SIGINT

# Keep script running
echo "⏳ Keeping subscribers running... Press Ctrl+C to stop"
wait
