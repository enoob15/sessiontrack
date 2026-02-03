#!/bin/bash

# Ensure script is run with sudo
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Update system packages
apt-get update
apt-get upgrade -y

# Install Docker and Docker Compose if not already installed
if ! command -v docker &> /dev/null; then
    apt-get install -y docker.io docker-compose
fi

# Navigate to project directory
cd /root/clawd/projects/sessiontrack

# Ensure directories exist
mkdir -p /root/clawd/sessions_archive
mkdir -p /root/clawd/projects/sessiontrack/project_data
mkdir -p /root/clawd/postgres_data

# Set appropriate permissions
chmod -R 755 /root/clawd/sessions_archive
chmod -R 755 /root/clawd/projects/sessiontrack/project_data
chmod -R 755 /root/clawd/postgres_data

# Stop any existing SessionTrack containers
docker-compose down

# Build and start services
docker-compose up --build -d

# Display running containers
docker ps | grep sessiontrack

# Print access information
echo "-------------------------------------------"
echo "SessionTrack Dashboard is now running:"
echo "Frontend: http://localhost:3025"
echo "Backend API: http://localhost:8005"
echo "PostgreSQL: localhost:5432"
echo "-------------------------------------------"

# Optional: Open in browser if graphical environment is available
if [[ -n "$DISPLAY" ]]; then
    xdg-open http://localhost:3025 || echo "Dashboard available at http://localhost:3025"
fi