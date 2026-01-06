"""
Google Gemini AI Client Wrapper  
Handles all communication with Google Gemini API using REST API.
Provides a clean interface for generating AI content.
"""

import httpx
from app.config import settings
from typing import Optional, Dict, Any
import json
import logging
import re

# Set up logging
logger = logging.getLogger(__name__)


class AIClient:
    """
    Google Gemini API client wrapper using REST API.
    """
    
    def __init__(self):
        """Initialize Gemini client with API key from settings."""
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self.max_tokens = settings.GEMINI_MAX_TOKENS
        self.temperature = settings.GEMINI_TEMPERATURE
        # Correct endpoint format for Gemini API v1 (not v1beta)
        self.base_url = f"https://generativelanguage.googleapis.com/v1/models/{self.model_name}:generateContent"
        logger.info(f"✅ AI Client initialized with model: {self.model_name}")
    
    async def generate_completion(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a completion from Google Gemini API using REST.
        
        Args:
            prompt: The prompt to send to the AI
            temperature: Randomness (0.0-1.0). Higher = more creative
            max_tokens: Maximum response length
            
        Returns:
            str: Generated text response
            
        Raises:
            Exception: If API call fails
        """
        try:
            url = f"{self.base_url}?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": temperature or self.temperature,
                    "maxOutputTokens": max_tokens or self.max_tokens,
                }
            }
            
            logger.info(f"🔄 Calling Gemini API: {self.model_name}")
            logger.debug(f"Prompt length: {len(prompt)} chars")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                
                # Log response status
                logger.info(f"📡 Gemini API Response Status: {response.status_code}")
                
                # Handle non-200 responses
                if response.status_code != 200:
                    error_detail = response.text
                    logger.error(f"❌ Gemini API Error ({response.status_code}): {error_detail}")
                    raise Exception(f"Gemini API returned {response.status_code}: {error_detail}")
                
                response.raise_for_status()
                data = response.json()
                
                # Extract text from response
                if "candidates" in data and len(data["candidates"]) > 0:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        text = candidate["content"]["parts"][0]["text"]
                        logger.info(f"✅ Successfully generated {len(text)} chars from Gemini")
                        return text.strip()
                
                logger.error("❌ No valid response structure from Gemini API")
                raise Exception("No valid response from Gemini API")
            
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ HTTP Status Error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Google Gemini API HTTP Error: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"❌ Request Error: {str(e)}")
            raise Exception(f"Network error calling Gemini API: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Unexpected error: {str(e)}")
            raise Exception(f"Google Gemini API Error: {str(e)}")
    
    async def generate_structured_json(
        self,
        prompt: str,
        temperature: Optional[float] = None
    ) -> Dict[Any, Any]:
        """
        Generate structured JSON response from Gemini.
        
        Args:
            prompt: The prompt requesting JSON output
            temperature: Randomness level
            
        Returns:
            dict: Parsed JSON response
            
        Raises:
            Exception: If API call fails or JSON parsing fails
        """
        try:
            # Add JSON formatting instruction to prompt
            json_prompt = f"{prompt}\n\nIMPORTANT: Return ONLY valid JSON, no additional text."
            
            logger.info("🔄 Generating structured JSON response")
            
            # Get completion
            response = await self.generate_completion(
                prompt=json_prompt,
                temperature=temperature
            )
            
            logger.debug(f"Raw response preview: {response[:200]}...")
            
            # Clean and extract JSON from response
            response = self._extract_json(response)
            
            # Parse the JSON
            parsed_data = json.loads(response)
            logger.info(f"✅ Successfully parsed JSON response")
            return parsed_data
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON Parse Error: {str(e)}")
            logger.error(f"Response was: {response[:500] if len(response) > 500 else response}")
            raise Exception(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error in generate_structured_json: {str(e)}")
            raise Exception(f"AI generation error: {str(e)}")
    
    def _extract_json(self, response: str) -> str:
        """
        Extract JSON from various response formats (markdown, code blocks, etc.)
        
        Args:
            response: Raw AI response
            
        Returns:
            str: Cleaned JSON string
        """
        # Remove leading/trailing whitespace
        response = response.strip()
        
        # Handle markdown code blocks
        if "```json" in response:
            logger.debug("Removing JSON markdown wrapper")
            # Extract content between ```json and ```
            parts = response.split("```json")
            if len(parts) > 1:
                response = parts[1].split("```")[0].strip()
        elif "```" in response:
            logger.debug("Removing generic markdown wrapper")
            # Extract content between ``` and ```
            parts = response.split("```")
            if len(parts) >= 3:
                response = parts[1].strip()
        
        # Remove any text before the first { or [
        json_start = response.find('{')
        if json_start == -1:
            json_start = response.find('[')
        if json_start > 0:
            logger.debug(f"Removing {json_start} chars before JSON start")
            response = response[json_start:]
        
        # Remove any text after the last } or ]
        json_end = response.rfind('}')
        if json_end == -1:
            json_end = response.rfind(']')
        if json_end > 0 and json_end < len(response) - 1:
            logger.debug(f"Removing {len(response) - json_end - 1} chars after JSON end")
            response = response[:json_end + 1]
        
        # Fix common JSON issues
        # Replace smart quotes with regular quotes
        response = response.replace('"', '"').replace('"', '"')
        response = response.replace(''', "'").replace(''', "'")
        
        # Remove any trailing commas before closing braces/brackets
        response = re.sub(r',(\s*[}\]])', r'\1', response)
        
        return response.strip()
    
    async def validate_api_key(self) -> bool:
        """
        Validate that the API key is working.
        
        Returns:
            bool: True if API key is valid, False otherwise
        """
        try:
            logger.info("🔍 Validating Gemini API key...")
            # Try a minimal API call
            await self.generate_completion("Say 'OK'", max_tokens=10)
            logger.info("✅ API key is valid")
            return True
        except Exception as e:
            logger.error(f"❌ API key validation failed: {str(e)}")
            return False


# Create global AI client instance
ai_client = AIClient()

