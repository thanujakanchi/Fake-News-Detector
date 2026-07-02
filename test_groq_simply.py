# test_groq_simple.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("❌ API Key not found!")
    exit()

client = Groq(api_key=api_key)

try:
    completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Say 'Groq is working' in 3 words"}
        ],
        model="llama-3.3-70b-versatile",
    )
    
    print("✅ Groq API is working!")
    print(f"Response: {completion.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")