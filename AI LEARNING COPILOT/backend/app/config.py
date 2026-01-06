"""
Configuration management for the CodeCore AI Backend.
Loads environment variables securely and provides centralized configuration.
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Centralized settings management.
    All sensitive data loaded from environment variables.
    """
    
    # API Configuration
    API_TITLE: str = "CodeCore AI Backend"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered educational content generation API"
    
    # Google Gemini AI Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # Latest stable model
    GEMINI_MAX_TOKENS: int = int(os.getenv("GEMINI_MAX_TOKENS", "2000"))
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8080",
        "*"  # Allow all origins in development (restrict in production)
    ]
    
    # Generation Limits
    MAX_TOPICS: int = int(os.getenv("MAX_TOPICS", "9"))
    QUESTIONS_PER_TOPIC: int = int(os.getenv("QUESTIONS_PER_TOPIC", "5"))
    
    def validate(self) -> bool:
        """
        Validate that required environment variables are set.
        Returns True if valid, raises ValueError otherwise.
        """
        if not self.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Please add it to your .env file or environment variables."
            )
        return True


# Create global settings instance
settings = Settings()

# Validate settings on import
try:
    settings.validate()
    print("[OK] Configuration loaded successfully")
except ValueError as e:
    print(f"[WARNING] Configuration Error: {e}")
    print("[INFO] Tip: Create a .env file with: GEMINI_API_KEY=your_key_here")
