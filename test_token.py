import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("HUGGINGFACE_API_KEY")
if token:
    print(f"✅ Token found: {token[:10]}...")
    print("✅ Token format looks correct")
else:
    print("❌ No token found in .env file")
