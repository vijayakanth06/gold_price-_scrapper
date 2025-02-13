#!/bin/bash
set -e

# Install Chromium (lightweight alternative to Google Chrome)
apt-get update && apt-get install -y chromium-browser

# Set Chromium path for Selenium
export CHROME_BIN=/usr/bin/chromium-browser

# Start Flask app
gunicorn -b 0.0.0.0:5000 app:app
