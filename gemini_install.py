import sys
import subprocess

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--break-system-packages"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package}: {e}")
        return False
    return True

def main():
    packages = [
        "google-generativeai",
        "google-ai-generativelanguage",
        "google-api-core",
        "google-api-python-client",
    ]

    for package in packages:
        print(f"Attempting to install {package}...")
        if install_package(package):
            print(f"{package} installed successfully.")
        else:
            print(f"Failed to install {package}")

    # Verify installation
    try:
        import google.generativeai
        print("Gemini library successfully imported!")
    except ImportError:
        print("Failed to import Gemini library")

if __name__ == "__main__":
    main()