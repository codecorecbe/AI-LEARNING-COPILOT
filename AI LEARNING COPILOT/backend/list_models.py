"""
List all available Gemini models
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("🔍 Fetching Available Gemini Models")
print("=" * 60)

# Try v1 API
print("\n📡 Checking v1 API...")
url_v1 = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

try:
    response = httpx.get(url_v1, timeout=30.0)
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Found {len(data.get('models', []))} models in v1 API:\n")
        for model in data.get('models', []):
            name = model.get('name', '').replace('models/', '')
            supported = model.get('supportedGenerationMethods', [])
            if 'generateContent' in supported:
                print(f"  ✅ {name} (supports generateContent)")
            else:
                print(f"  ⚠️ {name} (methods: {', '.join(supported)})")
    else:
        print(f"❌ v1 API failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error with v1 API: {str(e)}")

# Try v1beta API  
print("\n📡 Checking v1beta API...")
url_v1beta = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    response = httpx.get(url_v1beta, timeout=30.0)
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Found {len(data.get('models', []))} models in v1beta API:\n")
        for model in data.get('models', []):
            name = model.get('name', '').replace('models/', '')
            supported = model.get('supportedGenerationMethods', [])
            if 'generateContent' in supported:
                print(f"  ✅ {name} (supports generateContent)")
            else:
                print(f"  ⚠️  {name} (methods: {', '.join(supported)})")
    else:
        print(f"❌ v1beta API failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error with v1beta API: {str(e)}")

print("\n" + "=" * 60)
