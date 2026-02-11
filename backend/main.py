import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    print("WARNING: GENAI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=GENAI_API_KEY)

# Load Contacts
CONTACTS_DATA = []
try:
    with open("data/contacts.json", "r") as f:
        CONTACTS_DATA = json.load(f)
    print(f"Loaded {len(CONTACTS_DATA)} contacts.")
except Exception as e:
    print(f"Error loading contacts: {e}")

# System Prompt Construction
SYSTEM_PROMPT = f"""
You are MUJbot, the official AI assistant for Manipal University Jaipur (MUJ).
Your persona is a blend of a Marketing Agent, a Consulting Agent, and a College Counsellor.

**Your Responsibilities:**
1.  **Marketing**: Promote MUJ's strengths, campus life, and opportunities. Be enthusiastic and welcoming.
2.  **Consulting**: Answer queries about courses, placements, and facilities with accurate information.
3.  **Counselling**: Validate necessary courses based on student interest, passion, long-term goals, and high school achievements.
4.  **Receptionist**: Provide contact information for faculty and administration from your knowledge base.

**Knowledge Base (Contacts):**
{json.dumps(CONTACTS_DATA, indent=2)}

**Guidelines:**
- If satisfied with the user's query, provide the contact details directly from the knowledge base.
- If the user asks about courses, guide them based on their interests.
- Be polite, professional, and helpful.
- If you don't know an answer, suggest contacting the Helpdesk or Admissions team from the contact list.
- Do NOT make up information about specific people or phone numbers not in the list.

**Current Interaction:**
"""

# Gemini Model Generation Configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_PROMPT,
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not GENAI_API_KEY:
        # MOCK MODE
        import random
        query = request.message.lower()
        
        # Simple RAG Simulation
        matched_contacts = []
        for contact in CONTACTS_DATA:
            if (contact['role'] and contact['role'].lower() in query) or \
               (contact['name'] and contact['name'].lower() in query) or \
               (contact['category'] and contact['category'].lower() in query):
                matched_contacts.append(f"{contact['name']} ({contact['role']}): {contact['phone'] or contact['email']}")
        
        if matched_contacts:
            contact_info = "\n".join(matched_contacts[:3])
            return {"response": f"[MOCK MODE] Here is the contact info you asked for:\n{contact_info}"}
            
        # Persona Simulation
        if "course" in query or "study" in query:
            return {"response": "[MOCK MODE] MUJ offers world-class engineering, management, and arts courses! Based on your interest, I can suggest the best path for you. What subjects do you enjoy?"}
        elif "admission" in query:
             return {"response": "[MOCK MODE] Admissions are open! You can apply online. Do you need the contact of an admission counselor?"}
        else:
            responses = [
                "[MOCK MODE] Hello! I am MUJbot. How can I assist you with your university journey today?",
                "[MOCK MODE] Manipal University Jaipur is a great place to be! Ask me anything about campus life.",
                "[MOCK MODE] I can help you find faculty contacts or choose the right course."
            ]
            return {"response": random.choice(responses)}

    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(request.message)
        return {"response": response.text}
    except Exception as e:
        print(f"Gemini Error: {e}")
        # Fallback to mock if API fails
        return {"response": f"[MOCK ERROR] API Error: {str(e)}. (Running in fallback mode)"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
