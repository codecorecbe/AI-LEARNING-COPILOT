"""
Prompt Builder for AI Content Generation
Constructs intelligent prompts for topic and question generation.
"""

from app.config import settings
from typing import List


class PromptBuilder:
    """
    Build optimized prompts for educational content generation.
    """
    
    @staticmethod
    def build_topics_and_questions_prompt(subject: str) -> str:
        """
        Build a prompt to generate topics and questions for a subject.
        
        Args:
            subject: The subject name (e.g., "Python", "Data Science")
            
        Returns:
            str: Complete prompt for AI
        """
        max_topics = settings.MAX_TOPICS
        questions_per_topic = settings.QUESTIONS_PER_TOPIC
        
        prompt = f"""
You are an expert educational content creator. Generate learning content for: "{subject}"

TASK:
Generate {max_topics} comprehensive topics with {questions_per_topic} thought-provoking questions each.

REQUIREMENTS:
1. Topics should cover the subject from basic to advanced
2. Topics should be relevant, specific, and educational
3. Questions should be clear, engaging, and promote deep understanding
4. Questions should vary in type: conceptual, practical, comparative, and applied
5. Avoid yes/no questions - focus on "What", "How", "Why", "Explain"

OUTPUT FORMAT (strict JSON):
{{
  "topics": [
    {{
      "topic": "Topic Name 1",
      "questions": [
        "Question 1 text?",
        "Question 2 text?",
        "Question 3 text?",
        "Question 4 text?",
        "Question 5 text?"
      ]
    }},
    {{
      "topic": "Topic Name 2",
      "questions": [...]
    }}
  ]
}}

EXAMPLE for "Python Programming":
{{
  "topics": [
    {{
      "topic": "Python Fundamentals",
      "questions": [
        "What are the core data types in Python and when should each be used?",
        "How does Python's dynamic typing differ from static typing?",
        "Explain the concept of variables and naming conventions in Python",
        "What are the advantages of using Python for beginners?",
        "How do you handle user input and output in Python?"
      ]
    }},
    {{
      "topic": "Control Flow and Logic",
      "questions": [
        "How do if-elif-else statements work in Python?",
        "What is the difference between while and for loops?",
        "Explain how to use break and continue statements effectively",
        "How can you implement nested loops in Python?",
        "What are list comprehensions and when should you use them?"
      ]
    }}
  ]
}}

Now generate content for: "{subject}"

Return ONLY the JSON object, no additional text.
"""
        return prompt.strip()
    
    @staticmethod
    def build_questions_prompt(subject: str, topic: str, count: int = 5) -> str:
        """
        Build a prompt to generate only questions for a specific topic.
        
        Args:
            subject: The subject name
            topic: The specific topic within the subject
            count: Number of questions to generate
            
        Returns:
            str: Complete prompt for AI
        """
        prompt = f"""
Generate {count} educational questions about "{topic}" in the context of "{subject}".

REQUIREMENTS:
1. Questions should be clear and specific
2. Mix conceptual and practical questions
3. Avoid yes/no questions
4. Focus on understanding and application
5. Vary difficulty from beginner to intermediate

OUTPUT FORMAT (strict JSON):
{{
  "questions": [
    "Question 1 text?",
    "Question 2 text?",
    "Question 3 text?"
  ]
}}

Return ONLY the JSON object.
"""
        return prompt.strip()
    
    @staticmethod
    def build_quiz_prompt(topic: str, count: int = 5, difficulty: str = "medium") -> str:
        """
        Build a prompt for generating quiz questions with multiple choice answers.
        
        Args:
            topic: The topic for the quiz
            count: Number of questions
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            str: Complete prompt for AI
        """
        prompt = f"""
Generate {count} multiple-choice quiz questions about "{topic}".

DIFFICULTY: {difficulty}

REQUIREMENTS:
1. Each question should have 4 answer options (A, B, C, D)
2. Mark the correct answer
3. Include a brief explanation
4. Questions should test understanding, not just memorization

OUTPUT FORMAT (strict JSON):
{{
  "questions": [
    {{
      "question": "Question text?",
      "options": {{
        "A": "Option A text",
        "B": "Option B text",
        "C": "Option C text",
        "D": "Option D text"
      }},
      "correct_answer": "B",
      "explanation": "Brief explanation of why B is correct"
    }}
  ]
}}

Return ONLY the JSON object.
"""
        return prompt.strip()
    
    @staticmethod
    def build_doubt_answer_prompt(question: str, context: str = "") -> str:
        """
        Build a prompt for answering student doubts/questions.
        
        Args:
            question: The student's question
            context: Optional context about what the student is learning
            
        Returns:
            str: Complete prompt for AI
        """
        context_text = f"\nContext: Student is learning about {context}" if context else ""
        
        prompt = f"""
A student asked: "{question}"{context_text}

Provide a clear, helpful, and educational answer with relevant learning resources.

REQUIREMENTS:
1. Explain concepts clearly and simply (no code blocks or backticks in JSON values)
2. Use examples when helpful
3. Break down complex ideas into steps
4. Be encouraging and supportive
5. Keep the answer concise but complete (max 300 words)
6. Suggest 2 relevant YouTube videos that would help learn this topic

IMPORTANT: Do NOT use backticks, code fences, or special characters in the answer text.

OUTPUT FORMAT (strict JSON):
{{
  "answer": "Your detailed answer here with clear explanations. Do not use backticks or code blocks.",
  "key_points": [
    "Key point 1",
    "Key point 2",
    "Key point 3"
  ],
  "video_suggestions": [
    {{
      "title": "Video Title for Beginners",
      "description": "Brief description of what this video teaches",
      "search_query": "exact YouTube search term"
    }},
    {{
      "title": "Video Title for Practice",
      "description": "Brief description of what this video teaches",
      "search_query": "exact YouTube search term"
    }}
  ]
}}

Return ONLY the JSON object, no markdown formatting.
"""
        return prompt.strip()
    
    @staticmethod
    def build_quiz_generation_prompt(topic: str, count: int = 40) -> str:
        """
        Build a prompt to generate quiz questions for a specific topic.
        
        Args:
            topic: The topic for quiz generation
            count: Number of questions to generate (default: 40)
            
        Returns:
            str: Complete prompt for AI
        """
        prompt = f"""
You are an expert quiz creator. Generate {count} multiple-choice quiz questions about: "{topic}"

CRITICAL JSON FORMATTING RULES:
1. Return ONLY valid JSON, no markdown, no backticks, no code fences
2. Use standard double quotes " for all strings (no smart quotes)
3. No trailing commas after last items
4. Escape special characters properly in strings
5. Keep explanations under 50 words
6. No line breaks within string values

REQUIREMENTS:
1. Create diverse questions covering different aspects of {topic}
2. Questions should range from basic to advanced level
3. Each question must have exactly 4 options (A, B, C, D)
4. Only ONE correct answer per question
5. Include brief explanations for correct answers
6. Questions should test understanding, not just memorization
7. Mix question types: definitions, applications, comparisons, scenarios
8. Avoid ambiguous or trick questions

OUTPUT FORMAT (strict JSON):
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": {{
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
      }},
      "correct_answer": "B",
      "explanation": "Brief explanation why this is correct"
    }}
  ]
}}

Now generate exactly {count} quiz questions for: "{topic}"

IMPORTANT: Return ONLY the JSON object. No markdown, no explanations, no extra text.
"""
        return prompt.strip()

    @staticmethod
    def build_answer_verification_prompt(question: str, student_answer: str) -> str:
        """
        Build a prompt to verify if a student's answer is correct.
        
        Args:
            question: The question being answered
            student_answer: The student's answer
            
        Returns:
            str: Complete prompt for AI
        """
        prompt = f"""
You are an expert educational assessor. Your task is to evaluate a student's answer to a question.

QUESTION: "{question}"

STUDENT ANSWER: "{student_answer}"

TASK:
1. Evaluate if the student's answer is correct or partially correct
2. Provide constructive feedback explaining the correctness
3. If incorrect, provide the correct answer or key concepts
4. Be encouraging and educational in your feedback

OUTPUT FORMAT (strict JSON):
{{
  "is_correct": true/false,
  "feedback": "Explanation of correctness - be constructive and educational",
  "correct_answer": "What the correct answer should be (if student is wrong)"
}}

Important:
- is_correct must be a boolean (true or false)
- feedback should be 1-2 sentences
- Only include correct_answer if the student answer is wrong
- Return ONLY valid JSON, no markdown or extra text
- No smart quotes, no trailing commas

Now evaluate this answer:
"""
        return prompt.strip()


# Create global prompt builder instance
prompt_builder = PromptBuilder()
