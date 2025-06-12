#!/bin/bash
# running with multiple subscribers in background
# This script runs multiple subscribers in the background and a publisher to test message fanout 

echo "🔍 Quick Debug Test"
echo "=================="

echo "  1️⃣  Starting single subscriber in background..."
python subscriber.py &
SUB_PID=$!
echo "   Started subscriber (PID: $SUB_PID)"

echo " 2️⃣ Starting the second subscriber in background..."
python subscriber.py &
echo "   Started second subscriber (PID: $!)" 


echo " 3️⃣ Starting the third subscriber in background..."
python subscriber.py &
echo "   Started third subscriber (PID: $!)"


echo  "4️⃣  Waiting 3 seconds for subscriber to initialize..."
sleep 3


echo "5️⃣ Publishing messages..."
python publisher.py


echo " 6️⃣ Waiting 3 seconds for message processing..."
sleep 3


echo "7️⃣  Stopping subscriber..."
kill $SUB_PID 2>/dev/null


echo "✅ Test complete!"
echo "💡 If you saw 'Received:' messages above, subscribers are working!"
echo "💡 If not, there might be a connection or timing issue."
