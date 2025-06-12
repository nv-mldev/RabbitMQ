#!/bin/bash

# Simple script to run subscribers in foreground (visible output)
# Use multiple terminals or tmux/screen for this approach

echo "🚀 Starting subscribers in separate terminals..."
echo ""
echo "Open 4 separate terminals and run:"
echo "Terminal 1: python subscriber.py"
echo "Terminal 2: python subscriber.py" 
echo "Terminal 3: python subscriber.py"
echo "Terminal 4: python subscriber.py"
echo ""
echo "Then in a 5th terminal run:"
echo "python publisher.py"
echo ""
echo "This way you'll see all the output clearly!"
