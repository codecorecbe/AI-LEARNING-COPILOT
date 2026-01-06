"""
Test script to verify the JSON parsing fix
"""
import asyncio
import sys
sys.path.insert(0, 'e:/codecoreaisys/backend')

from app.ai.ai_client import ai_client

async def test():
    try:
        print("🔄 Testing content generation for Python...")
        from app.ai.prompt_builder import prompt_builder
        
        prompt = prompt_builder.build_topics_and_questions_prompt("Python")
        result = await ai_client.generate_structured_json(prompt)
        
        print(f"\n✅ SUCCESS!")
        print(f"Generated {len(result.get('topics', []))} topics")
        print(f"\nFirst topic: {result['topics'][0]['topic']}")
        print(f"First question: {result['topics'][0]['questions'][0]}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
