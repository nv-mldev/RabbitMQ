#!/bin/bash

# Real-time subscriber output viewer
# This script shows output from all subscribers in a organized way

echo "🔍 Real-time Subscriber Output Viewer"
echo "======================================"

# Check if log files exist
if [ ! -d "logs" ] || [ ! -f "logs/subscriber1.log" ]; then
    echo "❌ No log files found!"
    echo "💡 Run './run_with_logs.sh' first to generate logs"
    exit 1
fi

echo "📺 Watching subscriber outputs (Press Ctrl+C to stop)..."
echo ""

# Use multitail if available, otherwise fallback to tail
if command -v multitail &> /dev/null; then
    echo "🎯 Using multitail for better visualization..."
    multitail -l "tail -f logs/subscriber1.log" -l "tail -f logs/subscriber2.log" -l "tail -f logs/subscriber3.log" -l "tail -f logs/subscriber4.log"
else
    echo "📊 Showing combined output from all subscribers..."
    echo "💡 Install multitail for better visualization: sudo apt install multitail"
    echo ""
    tail -f logs/subscriber*.log
fi
