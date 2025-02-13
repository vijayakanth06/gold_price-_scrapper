#!/bin/bash
set -e

# Download Chrome without using sudo
mkdir -p $HOME/chrome
wget -q -O $HOME/chrome/chrome.zip https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_120.0.6099.129-1_amd64.deb
cd $HOME/chrome
dpkg-deb -x chrome.zip $HOME/chrome/
export PATH="$HOME/chrome/opt/google/chrome/:$PATH"

# Verify Chrome installation
$HOME/chrome/opt/google/chrome/google-chrome --version || echo "Chrome installation failed"

# Start Flask app
gunicorn -b 0.0.0.0:5000 app:app
