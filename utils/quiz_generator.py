from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json
import os
from dotenv import load_dotenv

load_dotenv()

class QuizGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def generate_quiz(self, text_content, num_questions=5, question_types=None):
        if question_types is None:
            question_types = ["multiple_choice", "true_false", "short_answer"]
        
        prompt = f"""
        Generate a quiz based on the following text content. The quiz should contain {num_questions} questions 
        with the following question types: {', '.join(question_types)}. 
        Include a mix of question types where possible.
        
        For each question, provide:
        - The question text
        - The correct answer
        - For multiple choice: 4 options including the correct one
        - For true/false: just the correct answer (True or False)
        - For short answer: a sample correct answer
        
        Format the output as a JSON object with the following structure:
        {{
            "quiz": [
                {{
                    "question": "question text",
                    "type": "question type",
                    "options": ["option1", "option2", ...],  // only for multiple_choice
                    "answer": "correct answer"
                }},
                ...
            ],
            "topics_covered": ["list of main topics covered in the quiz"]
        }}
        
        Text content:
        {text_content}
        """
        
        messages = [
            SystemMessage(content="You are an expert quiz generator for educational content."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm(messages)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback in case the response isn't proper JSON
            return {
                "quiz": [],
                "topics_covered": [],
                "error": "Failed to parse quiz questions. Please try again."
            }
