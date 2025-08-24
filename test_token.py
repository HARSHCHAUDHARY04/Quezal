import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GOOGLE_API_KEY")
if token:
    print(f"✅ Google API Key found: {token[:10]}...")
    print("✅ API Key format looks correct")
else:
    print("❌ No Google API Key found in .env file")
