#!/bin/bash
set -e

# Install Chrome without sudo
mkdir -p $HOME/chrome
wget -q -O $HOME/chrome/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg-deb -x $HOME/chrome/chrome.deb $HOME/chrome/
export PATH="$HOME/chrome/opt/google/chrome/:$PATH"

# Verify Chrome installation
$HOME/chrome/opt/google/chrome/google-chrome --version || echo "Chrome installation failed"

# Start Flask app
gunicorn -b 0.0.0.0:5000 app:app
