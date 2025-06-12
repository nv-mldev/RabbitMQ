#!/bin/bash

# Script to install Microsoft Cascadia Code font on macOS

# Define variables
RELEASE_URL="https://api.github.com/repos/microsoft/cascadia-code/releases/latest"
TEMP_DIR="/tmp/cascadia-code"
FONT_DIR="$HOME/Library/Fonts"

# Create temp directory
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR" || exit 1

# Get the latest release download URL
echo "Fetching latest Cascadia Code release..."
DOWNLOAD_URL=$(curl -s "$RELEASE_URL" | grep "browser_download_url.*CascadiaCode.*\.zip" | cut -d '"' -f 4)

if [ -z "$DOWNLOAD_URL" ]; then
    echo "Error: Could not find download URL for Cascadia Code"
    exit 1
fi

echo "Downloading Cascadia Code from: $DOWNLOAD_URL"
curl -L -o CascadiaCode.zip "$DOWNLOAD_URL"

# Extract the zip file
echo "Extracting font files..."
unzip -q CascadiaCode.zip

# Find and install TTF files
echo "Installing fonts to $FONT_DIR..."
find . -name "*.ttf" -exec cp -v {} "$FONT_DIR" \;

# Clean up
echo "Cleaning up..."
cd /
rm -rf "$TEMP_DIR"

echo "Cascadia Code font installation complete!"
echo "You may need to restart applications to see the new font."