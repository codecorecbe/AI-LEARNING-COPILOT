"""
Standalone Gemini API Test Script
Tests the Google Gemini API connection independently
"""

import httpx
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-pro")

print("=" * 60)
print("🧪 Gemini API Connection Test")
print("=" * 60)
print(f"📍 API Key: {API_KEY[:20]}..." if API_KEY else "❌ No API key found!")
print(f"🤖 Model: {MODEL_NAME}")
print("=" * 60)
print()

if not API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
    exit(1)

# Test endpoint
url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={API_KEY}"

# Test payload
payload = {
    "contents": [{
        "parts": [{
            "text": "Say 'Hello, API is working!' in one sentence."
        }]
    }],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 100
    }
}

print("🔄 Sending test request to Gemini API...")
print(f"📡 URL: https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent")
print()

try:
    # Make the request
    response = httpx.post(url, json=payload, timeout=30.0)
    
    print(f"📊 Response Status: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract text from response
        if "candidates" in data and len(data["candidates"]) > 0:
            candidate = data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                text = candidate["content"]["parts"][0]["text"]
                print("✅ SUCCESS! API is working!")
                print(f"📝 Response: {text}")
                print()
                print("=" * 60)
                print("✅ Your Gemini API configuration is CORRECT!")
                print("=" * 60)
            else:
                print("⚠️ Unexpected response structure")
                print(json.dumps(data, indent=2))
        else:
            print("⚠️ No candidates in response")
            print(json.dumps(data, indent=2))
    else:
        print("❌ API Request Failed!")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print()
        
        # Parse error if JSON
        try:
            error_data = response.json()
            if "error" in error_data:
                error = error_data["error"]
                print("=" * 60)
                print("❌ ERROR DETAILS:")
                print(f"Code: {error.get('code')}")
                print(f"Status: {error.get('status')}")
                print(f"Message: {error.get('message')}")
                print("=" * 60)
                print()
                
                # Provide helpful suggestions
                if error.get('code') == 404:
                    print("💡 SOLUTION:")
                    print(f"   The model '{MODEL_NAME}' is not available.")
                    print("   Try these models instead:")
                    print("   - gemini-pro (recommended)")
                    print("   - gemini-1.5-pro")
                    print()
                    print("   Update your .env file:")
                    print("   GEMINI_MODEL=gemini-pro")
                elif error.get('code') == 400:
                    print("💡 SOLUTION:")
                    print("   Check your API key is valid")
                    print("   Get a key from: https://makersuite.google.com/app/apikey")
                elif error.get('code') == 429:
                    print("💡 SOLUTION:")
                    print("   Rate limit exceeded. Wait a moment and try again.")
        except:
            pass
            
except httpx.RequestError as e:
    print(f"❌ Network Error: {str(e)}")
    print("💡 Check your internet connection")
except Exception as e:
    print(f"❌ Unexpected Error: {str(e)}")

print()
print("=" * 60)
print("Test completed!")
print("=" * 60)
