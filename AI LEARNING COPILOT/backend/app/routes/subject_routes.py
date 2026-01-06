"""
API Routes for Subject/Topic/Question Generation
All endpoints for AI content generation.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import GenerateRequest, GenerateResponse, ErrorResponse
from app.services.subject_service import subject_service
from app.utils.response_helper import response_helper
from typing import Dict, Any
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateResponse,
    responses={
        200: {"description": "Successfully generated topics and questions"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Generate Topics and Questions",
    description="Generate AI-powered topics and questions for any subject"
)
async def generate_content(request: GenerateRequest):
    """
    Generate educational content for a subject.
    
    **Request Body:**
    - `subject`: Name of the subject (e.g., "Python", "Machine Learning")
    
    **Response:**
    - `subject`: Original subject name
    - `topics`: List of topics with questions
    - `total_topics`: Number of topics generated
    - `total_questions`: Total number of questions
    
    **Example Request:**
    ```json
    {
      "subject": "Python Programming"
    }
    ```
    
    **Example Response:**
    ```json
    {
      "subject": "Python Programming",
      "topics": [
        {
          "topic": "Python Basics",
          "questions": [
            "What is Python?",
            "How do you declare variables?"
          ]
        }
      ],
      "total_topics": 1,
      "total_questions": 2
    }
    ```
    """
    try:
        # Validate subject
        if not request.subject or len(request.subject.strip()) == 0:
            raise response_helper.error_response(
                error_type="ValidationError",
                message="Subject cannot be empty",
                status_code=400
            )
        
        # Generate content
        logger.info(f"API Request: Generate content for '{request.subject}'")
        result = await subject_service.generate_content(request.subject)
        
        logger.info(f"API Response: Generated {result.total_topics} topics successfully")
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in /generate: {str(e)}")
        raise response_helper.handle_service_error(e, "Content Generation")


@router.post(
    "/generate-questions",
    summary="Generate Questions for Topic",
    description="Generate specific questions for a given subject and topic"
)
async def generate_questions(
    subject: str,
    topic: str,
    count: int = 5
) -> Dict[str, Any]:
    """
    Generate questions for a specific topic.
    
    **Query Parameters:**
    - `subject`: Subject name
    - `topic`: Topic within the subject
    - `count`: Number of questions to generate (default: 5)
    
    **Example:**
    `/api/generate-questions?subject=Python&topic=Functions&count=3`
    """
    try:
        # Validate inputs
        response_helper.validate_request(
            subject and topic,
            "Subject and topic are required"
        )
        response_helper.validate_request(
            1 <= count <= 20,
            "Count must be between 1 and 20"
        )
        
        # Generate questions
        logger.info(f"Generating {count} questions for {subject} - {topic}")
        result = await subject_service.generate_topic_questions(subject, topic, count)
        
        return response_helper.success_response(result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /generate-questions: {str(e)}")
        raise response_helper.handle_service_error(e, "Question Generation")


@router.post(
    "/generate-quiz",
    summary="Generate Quiz",
    description="Generate a multiple-choice quiz for a topic"
)
async def generate_quiz(
    topic: str,
    count: int = 10
) -> Dict[str, Any]:
    """
    Generate a quiz with multiple choice questions.
    
    **Query Parameters:**
    - `topic`: Quiz topic
    - `count`: Number of questions (default: 10)
    
    **Example:**
    `/api/generate-quiz?topic=Python Functions&count=10`
    """
    try:
        # Validate inputs
        response_helper.validate_request(topic, "Topic is required")
        response_helper.validate_request(
            1 <= count <= 50,
            "Count must be between 1 and 50"
        )
        
        # Generate quiz
        logger.info(f"Generating {count} quiz questions for {topic}")
        result = await subject_service.generate_quiz(topic, count)
        
        return response_helper.success_response(result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /generate-quiz: {str(e)}")
        raise response_helper.handle_service_error(e, "Quiz Generation")


@router.post(
    "/answer-doubt",
    summary="Answer Student Doubt",
    description="Get AI-powered answer to a student's question"
)
async def answer_doubt(
    question: str,
    context: str = ""
) -> Dict[str, Any]:
    """
    Answer a student's doubt/question.
    
    **Query Parameters:**
    - `question`: The student's question
    - `context`: Optional context (e.g., "Python programming")
    
    **Example:**
    `/api/answer-doubt?question=What is a variable?&context=Python`
    """
    try:
        # Validate input
        response_helper.validate_request(question, "Question is required")
        
        # Answer doubt
        logger.info(f"Answering doubt: {question[:50]}...")
        result = await subject_service.answer_doubt(question, context)
        
        return response_helper.success_response(result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /answer-doubt: {str(e)}")
        raise response_helper.handle_service_error(e, "Doubt Answering")


@router.post(
    "/verify-answer",
    summary="Verify Student Answer",
    description="Check if a student's answer to a question is correct using AI"
)
async def verify_answer(
    question: str,
    answer: str
) -> Dict[str, Any]:
    """
    Verify if a student's answer is correct.
    
    **Query Parameters:**
    - `question`: The question being answered
    - `answer`: The student's answer
    
    **Response:**
    - `is_correct`: Boolean indicating if answer is correct
    - `feedback`: Explanation of correctness
    
    **Example:**
    `/api/verify-answer?question=What is a variable?&answer=A named container that stores a value`
    """
    try:
        # Validate inputs
        response_helper.validate_request(question, "Question is required")
        response_helper.validate_request(answer, "Answer is required")
        
        # Verify answer using AI
        logger.info(f"Verifying answer for: {question[:50]}...")
        result = await subject_service.verify_answer(question, answer)
        
        return response_helper.success_response(result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /verify-answer: {str(e)}")
        raise response_helper.handle_service_error(e, "Answer Verification")

