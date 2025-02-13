#!/bin/bash
set -e

# Install Google Chrome (latest stable)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Start the Flask app
gunicorn -b 0.0.0.0:5000 app:app
