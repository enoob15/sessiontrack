import os
import sys
import json

def check_gemini_configuration():
    print("🔍 Gemini API Configuration Diagnostic")
    print("=====================================")

    # Check Clawdbot configuration
    try:
        with open('/root/.clawdbot/clawdbot.json', 'r') as f:
            config = json.load(f)
            print("\n🔑 Clawdbot Configuration:")
            print(f"Gemini API Key Present: {bool(config.get('env', {}).get('GEMINI_API_KEY'))}")
            print(f"Gemini API Key (first 5 chars): {config.get('env', {}).get('GEMINI_API_KEY', '')[:5]}...")
    except Exception as e:
        print(f"❌ Error reading Clawdbot config: {e}")

    # Check environment variable
    print("\n🌍 Environment Variables:")
    gemini_key = os.getenv('GEMINI_API_KEY')
    print(f"GEMINI_API_KEY Present: {bool(gemini_key)}")
    print(f"GEMINI_API_KEY (first 5 chars): {gemini_key[:5]}..." if gemini_key else "Not set")

    # Attempt Gemini library import
    print("\n🐍 Python Library Check:")
    try:
        import google.generativeai as genai
        print("✅ google-generativeai library imported successfully")

        # Configure and test
        if gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                models = genai.list_models()
                print("\n📦 Available Gemini Models:")
                for model in models:
                    print(f"- {model.name}")
            except Exception as e:
                print(f"❌ Model listing failed: {e}")
        else:
            print("❌ Cannot configure: No API key found")

    except ImportError as e:
        print(f"❌ Library import failed: {e}")

if __name__ == "__main__":
    check_gemini_configuration()