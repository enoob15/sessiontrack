#!/bin/bash

# System and Network Diagnostic Script

echo "🔍 Comprehensive System Diagnostic Report"
echo "======================================="

# Python Information
echo -e "\n📋 Python Environment"
echo "--------------------"
which python3
python3 --version
python3 -m pip --version

# Package Management
echo -e "\n📦 Package Management"
echo "---------------------"
apt-cache policy python3-pip
apt-cache policy python3-dev

# Network Connectivity
echo -e "\n🌐 Network Diagnostics"
echo "---------------------"
echo "Resolving package repositories..."
apt-get update

# Check specific repository connectivity
echo -e "\n🔗 Repository Status"
echo "-------------------"
curl -v https://pypi.org/simple/ 2>&1 | grep "Connected to"
curl -v https://files.pythonhosted.org 2>&1 | grep "Connected to"

# System Configuration
echo -e "\n⚙️ System Configuration"
echo "----------------------"
uname -a
lsb_release -a

# Pip Configuration
echo -e "\n🐍 Pip Configuration"
echo "--------------------"
python3 -m site --user-site
python3 -m site --user-base

# Potential Conflict Detection
echo -e "\n🧩 Potential Conflicts"
echo "---------------------"
python3 -c "import sys; print('\n'.join(sys.path))"

# Permissions Check
echo -e "\n🔐 Permission Diagnostic"
echo "------------------------"
ls -l $(which python3)
ls -l $(which pip3)

echo -e "\n🏁 Diagnostic Complete"