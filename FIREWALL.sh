#!/bin/bash

# Ensure script is run with sudo
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Install UFW if not already installed
if ! command -v ufw &> /dev/null; then
    apt-get update
    apt-get install -y ufw
fi

# Allow SSH
ufw allow ssh

# Allow SessionTrack ports
ufw allow 3025/tcp  # Frontend (changed from 3000)
ufw allow 8000/tcp  # Backend API
ufw allow 5432/tcp  # PostgreSQL (optional, for external access)

# Enable firewall
ufw --force enable

# Show current firewall status
ufw status verbose