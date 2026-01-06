"""
Subject Service Layer
Business logic for generating educational content.
"""

from app.ai.ai_client import ai_client
from app.ai.prompt_builder import prompt_builder
from app.models.schemas import GenerateResponse, Topic
from typing import Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubjectService:
    """
    Service for handling subject-related operations.
    """
    
    @staticmethod
    async def generate_content(subject: str) -> GenerateResponse:
        """
        Generate topics and questions for a given subject.
        
        Args:
            subject: The subject name
            
        Returns:
            GenerateResponse: Structured response with topics and questions
            
        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"Generating content for subject: {subject}")
            
            # Build the prompt
            prompt = prompt_builder.build_topics_and_questions_prompt(subject)
            
            # Get AI-generated content
            ai_response = await ai_client.generate_structured_json(prompt)
            
            # Validate response structure
            if "topics" not in ai_response:
                raise ValueError("AI response missing 'topics' field")
            
            # Parse topics and questions
            topics_data = ai_response["topics"]
            topics = []
            total_questions = 0
            
            for topic_data in topics_data:
                topic_name = topic_data.get("topic", "Unnamed Topic")
                questions = topic_data.get("questions", [])
                
                # Ensure questions is a list
                if not isinstance(questions, list):
                    questions = []
                
                topics.append(Topic(
                    topic=topic_name,
                    questions=questions
                ))
                total_questions += len(questions)
            
            # Create response
            response = GenerateResponse(
                subject=subject,
                topics=topics,
                total_topics=len(topics),
                total_questions=total_questions
            )
            
            logger.info(
                f"Successfully generated {len(topics)} topics "
                f"with {total_questions} questions for {subject}"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating content for {subject}: {str(e)}")
            raise Exception(f"Content generation failed: {str(e)}")
    
    @staticmethod
    async def generate_topic_questions(
        subject: str,
        topic: str,
        count: int = 5
    ) -> Dict[str, Any]:
        """
        Generate questions for a specific topic.
        
        Args:
            subject: The subject name
            topic: The topic name
            count: Number of questions to generate
            
        Returns:
            dict: Questions data
        """
        try:
            logger.info(f"Generating {count} questions for {subject} - {topic}")
            
            # Build prompt
            prompt = prompt_builder.build_questions_prompt(subject, topic, count)
            
            # Get AI response
            ai_response = await ai_client.generate_structured_json(prompt)
            
            # Validate and return
            if "questions" not in ai_response:
                raise ValueError("AI response missing 'questions' field")
            
            return {
                "subject": subject,
                "topic": topic,
                "questions": ai_response["questions"]
            }
            
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            raise Exception(f"Question generation failed: {str(e)}")
    
    @staticmethod
    async def generate_quiz(
        topic: str,
        count: int = 40
    ) -> Dict[str, Any]:
        """
        Generate a quiz with multiple choice questions.
        
        Args:
            topic: Quiz topic
            count: Number of questions (default 40)
            
        Returns:
            dict: Quiz data with questions and answers
        """
        try:
            logger.info(f"Generating {count} quiz questions for {topic}")
            
            # Build prompt
            prompt = prompt_builder.build_quiz_generation_prompt(topic, count)
            
            # Get AI response
            ai_response = await ai_client.generate_structured_json(prompt)
            
            # Validate and return
            if "questions" not in ai_response:
                raise ValueError("AI response missing 'questions' field")
            
            return {
                "topic": topic,
                "total_questions": len(ai_response["questions"]),
                "questions": ai_response["questions"]
            }
            
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            raise Exception(f"Quiz generation failed: {str(e)}")
    
    @staticmethod
    async def answer_doubt(
        question: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Answer a student's doubt/question.
        
        Args:
            question: Student's question
            context: Optional learning context
            
        Returns:
            dict: Answer with key points and video suggestions
        """
        try:
            logger.info(f"Answering doubt: {question[:50]}...")
            
            # Build prompt
            prompt = prompt_builder.build_doubt_answer_prompt(question, context)
            
            # Get AI response
            ai_response = await ai_client.generate_structured_json(prompt)
            
            # Validate and return
            if "answer" not in ai_response:
                raise ValueError("AI response missing 'answer' field")
            
            return {
                "question": question,
                "answer": ai_response.get("answer", ""),
                "key_points": ai_response.get("key_points", []),
                "video_suggestions": ai_response.get("video_suggestions", [])
            }
            
        except Exception as e:
            logger.error(f"Error answering doubt: {str(e)}")
            raise Exception(f"Doubt answering failed: {str(e)}")
    
    @staticmethod
    async def verify_answer(
        question: str,
        answer: str
    ) -> Dict[str, Any]:
        """
        Verify if a student's answer is correct using AI.
        
        Args:
            question: The question being answered
            answer: The student's answer
            
        Returns:
            dict: Verification result with is_correct and feedback
        """
        try:
            logger.info(f"Verifying answer for: {question[:50]}...")
            
            # Build prompt for verification
            prompt = prompt_builder.build_answer_verification_prompt(question, answer)
            
            # Get AI response
            ai_response = await ai_client.generate_structured_json(prompt)
            
            # Validate and return
            if "is_correct" not in ai_response:
                raise ValueError("AI response missing 'is_correct' field")
            
            return {
                "question": question,
                "answer": answer,
                "is_correct": ai_response.get("is_correct", False),
                "feedback": ai_response.get("feedback", "Answer verified by AI"),
                "correct_answer": ai_response.get("correct_answer", "")
            }
            
        except Exception as e:
            logger.error(f"Error verifying answer: {str(e)}")
            raise Exception(f"Answer verification failed: {str(e)}")


# Create global service instance
subject_service = SubjectService()
