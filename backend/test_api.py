import os
import google.generativeai as genai
from dotenv import load_dotenv

# Force reload of .env
load_dotenv(override=True)

api_key = os.getenv("GENAI_API_KEY")
print(f"Loaded API Key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("ERROR: API Key is missing or empty.")
    exit(1)

genai.configure(api_key=api_key)

try:
    models = genai.list_models()
    print("Available Models:")
    for model in models:
        print(f"- {model.name}")
        
    model = genai.GenerativeModel('gemini-1.5-flash-latest') # Trying likely correct name
    response = model.generate_content("Hello")
    print(f"SUCCESS! Response: {response.text}")

except Exception as e:
    print(f"FAILED to connect to Gemini: {e}")
