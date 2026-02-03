#!/bin/bash
# Setup script for SessionTrack project

# Ensure Python and pip are installed
apt-get update
apt-get install -y python3 python3-pip python3-venv python3-dev build-essential

# Create virtual environment
python3 -m venv /root/clawd/projects/sessiontrack/venv
source /root/clawd/projects/sessiontrack/venv/bin/activate

# Install dependencies using pip with system packages
pip install --break-system-packages google-generativeai

# Set Gemini API Key
export GEMINI_API_KEY=$(jq -r '.env.GEMINI_API_KEY' /root/.clawdbot/clawdbot.json)

# Make CLI executable
chmod +x /root/clawd/projects/sessiontrack/backend/capture_cli.py

echo "SessionTrack environment setup complete!"