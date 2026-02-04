#!/usr/bin/env python3
import os
import sys
import subprocess
import importlib.util

def is_module_available(module_name):
    """Check if a module is available."""
    return importlib.util.find_spec(module_name) is not None

def install_with_pip(package):
    """Install a package using pip with specific flags."""
    try:
        result = subprocess.run([
            sys.executable, 
            "-m", "pip", 
            "install", 
            package, 
            "--break-system-packages",
            "--no-deps",
            "--force-reinstall"
        ], capture_output=True, text=True)
        
        print(f"Installation attempt for {package}:")
        print(result.stdout)
        print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error installing {package}: {e}")
        return False

def manually_download_and_install():
    """Manually download and install Gemini library."""
    try:
        # Download specific versions
        packages = [
            "https://files.pythonhosted.org/packages/35/35/42c4c44430d37ae9a3125c1ac43e332d5a5a6dd4b440c05466a46ae32bbf/google_generativeai-0.8.6-py3-none-any.whl",
            "https://files.pythonhosted.org/packages/f8/b3/e9/3c7b0a9c9de15acb7e15a8906e239e97c58bca72007363cba0a92c27047/google_ai_generativelanguage-0.6.15-py3-none-any.whl"
        ]
        
        for url in packages:
            filename = url.split("/")[-1]
            download_cmd = f"wget {url}"
            install_cmd = f"{sys.executable} -m pip install {filename} --break-system-packages --no-deps"
            
            print(f"Downloading: {url}")
            os.system(download_cmd)
            
            print(f"Installing: {filename}")
            os.system(install_cmd)
        
        return True
    except Exception as e:
        print(f"Manual installation error: {e}")
        return False

def verify_installation():
    """Verify Gemini library installation."""
    try:
        import google.generativeai as genai
        print("✅ Gemini library successfully imported!")
        
        # Attempt configuration
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
    print("🚀 Gemini Library Manual Installation")
    print("===================================")
    
    if is_module_available('google.generativeai'):
        print("✅ Gemini library already installed")
        sys.exit(0)
    
    # Attempt pip installation with custom flags
    if install_with_pip('google-generativeai'):
        if verify_installation():
            sys.exit(0)
    
    # Fallback to manual download and install
    if manually_download_and_install():
        if verify_installation():
            sys.exit(0)
    
    print("\n❌ Gemini library installation failed")
    sys.exit(1)

if __name__ == "__main__":
    main()