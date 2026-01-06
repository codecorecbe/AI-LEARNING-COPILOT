"""
Test the JSON extraction specifically
"""
import sys
sys.path.insert(0, 'e:/codecoreaisys/backend')

from app.ai.ai_client import ai_client
import json

# Read the saved response
with open('e:/codecoreaisys/ai_response_debug.txt', 'r', encoding='utf-8') as f:
    raw_response = f.read()

print("📝 Testing JSON extraction...")
print(f"Raw response length: {len(raw_response)}")

# Test the extraction
try:
    cleaned = ai_client._extract_json(raw_response)
    print(f"\n✅ Cleaned JSON length: {len(cleaned)}")
    print("\nCleaned JSON preview (first 300 chars):")
    print(cleaned[:300])
    print("\n" + "="*60)
    
    # Try to parse it
    parsed = json.loads(cleaned)
    print(f"\n✅ SUCCESS! Parsed {len(parsed.get('topics', []))} topics")
    print(f"\nFirst topic: {parsed['topics'][0]['topic']}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
