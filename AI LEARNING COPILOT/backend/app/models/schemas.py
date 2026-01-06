"""
Pydantic Models (Schemas) for Request/Response Validation
These models define the structure of data coming in and going out of the API.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional


class GenerateRequest(BaseModel):
    """
    Request model for /api/generate endpoint.
    User provides a subject name to generate topics and questions for.
    """
    subject: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Subject name (e.g., Python, JavaScript, Data Science)"
    )
    
    @validator('subject')
    def validate_subject(cls, v):
        """Validate and clean subject input"""
        # Remove extra whitespace
        v = v.strip()
        
        # Ensure not empty after stripping
        if not v:
            raise ValueError("Subject cannot be empty")
        
        return v


class Question(BaseModel):
    """
    Model for a single question.
    """
    question: str = Field(..., description="The generated question text")


class Topic(BaseModel):
    """
    Model for a topic with its associated questions.
    """
    topic: str = Field(..., description="Topic name")
    questions: List[str] = Field(
        ...,
        description="List of questions for this topic"
    )


class GenerateResponse(BaseModel):
    """
    Response model for /api/generate endpoint.
    Returns the subject with generated topics and questions.
    """
    subject: str = Field(..., description="Original subject name")
    topics: List[Topic] = Field(
        ...,
        description="List of generated topics with questions"
    )
    total_topics: int = Field(..., description="Total number of topics generated")
    total_questions: int = Field(..., description="Total number of questions generated")


class ErrorResponse(BaseModel):
    """
    Error response model for API errors.
    """
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Detailed error message")
    details: Optional[str] = Field(None, description="Additional error details")


# Example usage in documentation (Pydantic v2)
GenerateRequest.model_config = {
    "json_schema_extra": {
        "example": {
            "subject": "Python Programming"
        }
    }
}

GenerateResponse.model_config = {
    "json_schema_extra": {
        "example": {
            "subject": "Python Programming",
            "topics": [
                {
                    "topic": "Python Basics",
                    "questions": [
                        "What is Python and why is it popular?",
                        "How do you declare variables in Python?",
                        "What are Python data types?"
                    ]
                },
                {
                    "topic": "Python Functions",
                    "questions": [
                        "How do you define a function in Python?",
                        "What are function parameters and arguments?",
                        "Explain lambda functions in Python"
                    ]
                }
            ],
            "total_topics": 2,
            "total_questions": 6
        }
    }
}
