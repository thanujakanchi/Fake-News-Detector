# test_groq_web.py - SHORT VERSION to avoid 413 error
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

try:
    # KEEP THE PROMPT SHORT
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Fact-check claims. Be brief."},
            {"role": "user", "content": "Is 'humans speak' true?"}  # Short query
        ],
        model="groq/compound",
        max_tokens=200,  # Limit response
    )
    
    print("🔍 GROQ WEB SEARCH RESPONSE:")
    print("=" * 60)
    print(completion.choices[0].message.content)
    
except Exception as e:
    print(f"❌ Error: {e}")