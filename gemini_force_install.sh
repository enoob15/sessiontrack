#!/bin/bash

# Force Gemini Library Installation Script

# Ensure we're using the correct Python and Pip
PYTHON=$(which python3)
PIP=$(which pip3)

# Install dependencies with explicit package management
echo "🔧 Installing Gemini Library Dependencies"
$PIP install --break-system-packages \
    google-generativeai \
    google-ai-generativelanguage \
    google-api-core \
    google-api-python-client \
    pydantic \
    protobuf

# Verify installation
echo -e "\n🕵️ Verifying Gemini Library"
$PYTHON -c "
import sys
try:
    import google.generativeai as genai
    print('✅ Gemini library successfully imported!')
    
    # Attempt to configure with environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        print('\n📦 Available Gemini Models:')
        for model in models:
            print(f'  - {model.name}')
    else:
        print('⚠️ Gemini API key not found in environment')
except ImportError as e:
    print(f'❌ Gemini library import failed: {e}')
    sys.exit(1)
"