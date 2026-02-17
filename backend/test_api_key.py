
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    print("Error: GENAI_API_KEY not found.")
    exit(1)

print(f"Testing API Key: {api_key[:5]}...{api_key[-5:]}")



try:
    genai.configure(api_key=api_key)
    model_name = "gemini-flash-latest"
    print(f"Testing model: {model_name}")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello! Are you working?")
    print(f"Success! API Key works with {model_name}.")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error with {model_name}: {e}")
