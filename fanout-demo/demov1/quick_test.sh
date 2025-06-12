#!/bin/bash

echo "🔍 Quick Debug Test"
echo "=================="

echo "1️⃣  Starting single subscriber in background..."
python subscriber.py &
SUB_PID=$!
echo "   Started subscriber (PID: $SUB_PID)"

echo ""
echo "2️⃣  Waiting 3 seconds for subscriber to initialize..."
sleep 3

echo ""
echo "3️⃣  Publishing messages..."
python publisher.py

echo ""
echo "4️⃣  Waiting 2 seconds for message processing..."
sleep 2

echo ""
echo "5️⃣  Stopping subscriber..."
kill $SUB_PID 2>/dev/null

echo ""
echo "✅ Test complete!"
echo "💡 If you saw 'Received:' messages above, subscribers are working!"
echo "💡 If not, there might be a connection or timing issue."
