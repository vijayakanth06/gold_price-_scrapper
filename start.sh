#!/bin/bash

# Exit on any error
set -e

# Install dependencies
pip install -r requirements.txt

# Ensure Chromium is installed (Render provides it)
CHROME_PATH="/usr/bin/chromium"
if [ ! -f "$CHROME_PATH" ]; then
    echo "Chromium not found! Exiting..."
    exit 1
fi

# Start the Flask app
gunicorn -b 0.0.0.0:5000 app:app
