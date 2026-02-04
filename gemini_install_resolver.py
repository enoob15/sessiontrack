#!/usr/bin/env python3
import sys
import subprocess
import os
import importlib.metadata

def run_command(command, shell=False):
    """Run a shell command and return output or raise an exception."""
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            shell=shell
        )
        if result.returncode != 0:
            print(f"Command failed: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def diagnose_python_environment():
    """Provide a detailed diagnosis of the Python environment."""
    print("🔍 Python Environment Diagnosis")
    print("===============================")
    
    # Python version
    print(f"\n📌 Python Version: {sys.version}")
    
    # Python executable
    print(f"📂 Python Executable: {sys.executable}")
    
    # Site packages
    import site
    print("\n📦 Site Packages Locations:")
    for path in site.getsitepackages():
        print(f"  - {path}")
    
    # Existing package conflicts
    print("\n🧩 Existing Package Conflicts:")
    try:
        typing_ext_version = importlib.metadata.version('typing-extensions')
        print(f"  - typing_extensions: {typing_ext_version}")
    except Exception as e:
        print(f"  - Unable to retrieve typing_extensions version: {e}")

def uninstall_conflicting_packages():
    """Attempt to remove conflicting packages."""
    print("\n🔧 Attempting to Remove Conflicting Packages")
    commands = [
        [sys.executable, "-m", "pip", "uninstall", "-y", "typing_extensions"],
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        [sys.executable, "-m", "pip", "install", "--upgrade", "setuptools"],
    ]
    
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"Command failed: {result.stderr}")

def install_gemini_library():
    """Attempt to install Gemini library with various strategies."""
    print("\n📥 Installing Gemini Library")
    
    # Different installation strategies
    install_strategies = [
        [sys.executable, "-m", "pip", "install", "google-generativeai", "--break-system-packages"],
        [sys.executable, "-m", "pip", "install", "google-generativeai", "--user"],
        [sys.executable, "-m", "pip", "install", "google-generativeai", "--upgrade"],
    ]
    
    for strategy in install_strategies:
        print(f"\nTrying strategy: {' '.join(strategy)}")
        result = subprocess.run(
            strategy, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Installation successful!")
            return True
        else:
            print("❌ Installation failed")
            print(result.stderr)
    
    return False

def verify_gemini_installation():
    """Verify Gemini library installation."""
    print("\n🕵️ Verifying Gemini Library Installation")
    try:
        import google.generativeai as genai
        print("✅ Gemini library successfully imported!")
        
        # Additional verification
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            models = genai.list_models()
            print("\n📦 Available Gemini Models:")
            for model in models:
                print(f"  - {model.name}")
        else:
            print("⚠️ Gemini API key not found in environment")
        
        return True
    except ImportError as e:
        print(f"❌ Gemini library import failed: {e}")
        return False

def main():
    print("🚀 Gemini Library Installation Resolver")
    print("======================================")
    
    diagnose_python_environment()
    uninstall_conflicting_packages()
    
    if install_gemini_library():
        if verify_gemini_installation():
            print("\n🎉 Gemini library successfully installed and verified!")
            sys.exit(0)
    
    print("\n❌ Gemini library installation failed")
    sys.exit(1)

if __name__ == "__main__":
    main()