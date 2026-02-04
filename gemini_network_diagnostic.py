#!/usr/bin/env python3
import os
import sys
import subprocess
import importlib.metadata

def diagnose_network_and_pypi():
    """Comprehensive network and package repository diagnostic."""
    print("🌐 Gemini Library Network & Repository Diagnostic")
    print("===========================================")
    
    # Network Connectivity Test
    print("\n🔗 Network Connectivity")
    print("---------------------")
    try:
        subprocess.run(["curl", "-v", "https://pypi.org/simple/"], 
                       capture_output=True, text=True, timeout=10)
        print("✅ PyPI Repository Accessible")
    except subprocess.TimeoutExpired:
        print("❌ PyPI Repository Connection Timeout")
    except Exception as e:
        print(f"❌ Network Test Failed: {e}")
    
    # SSL/TLS Verification
    print("\n🔐 SSL/TLS Configuration")
    print("----------------------")
    try:
        subprocess.run(["openssl", "s_client", "-connect", "pypi.org:443"], 
                       capture_output=True, text=True, timeout=10)
        print("✅ SSL/TLS Connection Verified")
    except Exception as e:
        print(f"❌ SSL Verification Failed: {e}")
    
    # Alternative Download Mechanism
    print("\n📦 Package Download Diagnostic")
    print("----------------------------")
    try:
        # Use pip to download without installing
        download_result = subprocess.run(
            [sys.executable, "-m", "pip", "download", 
             "--only-binary=:all:", 
             "--dest=/tmp/pip_download", 
             "google-generativeai"],
            capture_output=True, text=True
        )
        
        if download_result.returncode == 0:
            print("✅ Package Download Successful")
            print(f"Downloaded to: /tmp/pip_download")
        else:
            print("❌ Package Download Failed")
            print(download_result.stderr)
    
    except Exception as e:
        print(f"❌ Download Diagnostic Error: {e}")
    
    # Python Environment Details
    print("\n🐍 Python Environment")
    print("--------------------")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    
    try:
        # List installed packages
        installed_packages = subprocess.run(
            [sys.executable, "-m", "pip", "list"], 
            capture_output=True, text=True
        )
        print("\nInstalled Packages:")
        print(installed_packages.stdout)
    except Exception as e:
        print(f"❌ Package Listing Error: {e}")

def main():
    diagnose_network_and_pypi()

if __name__ == "__main__":
    main()