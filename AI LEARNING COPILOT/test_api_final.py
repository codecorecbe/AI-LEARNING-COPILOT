import requests
import json
import time

# Wait for backend to be ready
print("⏳ Waiting for backend to be ready...")
time.sleep(3)

# Test the API
url = "http://localhost:8000/api/generate"
payload = {"subject": "Python"}
headers = {"Content-Type": "application/json"}

print(f"📡 Testing API: POST {url}")
print(f"📦 Payload: {json.dumps(payload)}\n")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API SUCCESS!")
        print(f"Subject: {data['subject']}")
        print(f"Topics: {data['total_topics']}")
        print(f"Questions: {data['total_questions']}")
        print(f"\nFirst topic: {data['topics'][0]['topic']}")
        print(f"First question: {data['topics'][0]['questions'][0]}")
        print("\n✅ THE FIX WORKS! Backend is generating content successfully.")
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
except Exception as e:
    print(f"❌ Error: {e}")
