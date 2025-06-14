#!/bin/bash

echo "Starting the demo run..."
# Ensure the script is run from the correct directory
cd "$(dirname "$0")/.."
# Check if the required Python scripts exist
if [[ ! -f "alarm_raiser.py" || ! -f "file_writer.py" || ! -f "screen_printer.py" || ! -f "publisher.py" ]]; then
    echo "One or more required Python scripts are missing."
    exit 1
fi
# Ensure the Python environment is set up
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    exit 1
fi



echo "Running the demo scripts..."

# Run alarm_raiser.py in the background
echo "Starting alarm_raiser..."
python3 alarm_raiser.py &
# Check if the alarm_raiser started successfully
if ! kill -0 $PID_ALARM 2>/dev/null; then
    echo "Failed to start alarm_raiser."
    exit 1
fi
PID_ALARM=$!

# Run file_writer in the background
echo "Starting file_writer..."
python3 file_writer.py 
# Check if the file_writer started successfully
if ! kill -0 $PID_FILE_WRITER 2>/dev/null; then
    echo "Failed to start file_writer."
    exit 1
fi
PID_FILE_WRITER=$!

# Run screen_printer in the background
echo "Starting screen_printer..."
python3 screen_printer.py &
# Check if the screen_printer started successfully
if ! kill -0 $PID_SCREEN_PRINTER 2>/dev/null; then
    echo "Failed to start screen_printer."
    exit 1
fi
PID_SCREEN_PRINTER=$!
# Wait a moment to ensure the above processes are running
sleep 2

# Run publisher
echo "Starting publisher..."
python3 publisher.py
# Check if the publisher started successfully
if [[ $? -ne 0 ]]; then
    echo "Failed to start publisher."
    exit 1
fi
# Wait for a moment to allow the publisher to run
PID_ALARM=$(jobs -p)

# Wait for all background processes to finish
# Set up cleanup function and trap before starting background processes
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}
trap cleanup SIGINT

wait
echo "Demo run completed successfully."
# Optionally, you can clean up background processes if needed
kill $(jobs -p) 2>/dev/null
echo "All processes have been terminated."

# Exit with success status
exit 0
# End of demo_run.sh
# This script is designed to run a demo of the selective alarm system.
# It starts multiple Python scripts in the background and waits for them to complete.
# The scripts are expected to be in the same directory as this script.
# Make sure to run this script from the root directory of the project.