#!/bin/bash

# Ensure required tools are installed
sudo apt-get update
sudo apt-get install -y docker.io docker-compose npm nodejs

# Clone the repository (if not already cloned)
if [ ! -d "/root/clawd/projects/sessiontrack" ]; then
    git clone https://github.com/enoob15/sessiontrack.git /root/clawd/projects/sessiontrack
fi

# Navigate to project directory
cd /root/clawd/projects/sessiontrack

# Install frontend dependencies
cd frontend
npm install
cd ..

# Build and start services
docker-compose up --build -d

# Open browser (if in a graphical environment)
xdg-open http://localhost:3000 || echo "Dashboard available at http://localhost:3000"