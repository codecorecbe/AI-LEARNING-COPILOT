"""
Test script to capture full AI response
"""
import asyncio
import sys
sys.path.insert(0, 'e:/codecoreaisys/backend')

from app.ai.ai_client import ai_client

async def test():
    try:
        print("🔄 Testing AI response capture...")
        
        # Simple test prompt
        prompt = 'Generate a JSON object with topics about Python. Format: {"topics": [{"topic": "name", "questions": ["q1", "q2"]}]}'
        
        # Get raw completion
        raw_response = await ai_client.generate_completion(prompt, max_tokens=4000)
        
        print(f"\n📝 Full Response Length: {len(raw_response)} chars")
        print(f"\n{'='*60}")
        print("FULL RESPONSE:")
        print(f"{'='*60}")
        print(raw_response)
        print(f"{'='*60}")
        
        # Save to file
        with open('e:/codecoreaisys/ai_response_debug.txt', 'w', encoding='utf-8') as f:
            f.write(raw_response)
        print(f"\n✅ Response saved to ai_response_debug.txt")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
