#!/bin/bash
set -e  # Stop on error

# Install dependencies
pip install -r requirements.txt

# Download and extract Chromium (if needed)
mkdir -p /tmp/chrome
cd /tmp/chrome
wget https://storage.googleapis.com/chrome-for-testing-public/120.0.6099.109/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
CHROME_PATH="/tmp/chrome/chrome-linux64/chrome"

# Verify Chromium installation
if [ ! -f "$CHROME_PATH" ]; then
    echo "Chromium download failed! Exiting..."
    exit 1
fi
echo "Chromium installed at $CHROME_PATH"

# Go back to project root
cd /opt/render/project/src

# Run Gunicorn (Make sure app.py exists)
gunicorn -b 0.0.0.0:5000 app:app --workers=3 --timeout=120

