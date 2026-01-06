#!/usr/bin/env python3
"""Test the backend API directly"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

async def test_api():
    from app.ai.ai_client import AIClient
    from app.config import settings
    
    print("Testing Google Gemini API...")
    print(f"API Key: {settings.GEMINI_API_KEY[:30]}...")
    print(f"Model: {settings.GEMINI_MODEL}")
    
    client = AIClient()
    
    try:
        prompt = "Generate 3 topics for learning Python basics. Format as JSON with 'topics' array."
        response = await client.generate_completion(prompt)
        print(f"\n✅ API Response:\n{response}")
        return True
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api())
    sys.exit(0 if success else 1)
