from transformers import pipeline, set_seed
import random

def generate_quiz(text, num_questions=5):
    # Use GPT-2 which has fewer dependencies
    generator = pipeline("text-generation", model="gpt2")
    
    set_seed(random.randint(1, 1000))
    prompt = f"Generate {num_questions} quiz questions about: {text[:500]}\n\n1."
    
    try:
        result = generator(prompt, max_length=500, num_return_sequences=1)
        questions = parse_questions(result[0]['generated_text'])
        return {
            "quiz": questions[:num_questions],
            "topics_covered": list(set([q.get('topic', 'General') for q in questions]))
        }
    except Exception as e:
        return {"error": str(e), "quiz": []}

def parse_questions(text):
    # Simple parsing logic (customize as needed)
    questions = []
    for q in text.split("\n"):
        if "?" in q:
            parts = q.split("?")
            questions.append({
                "question": parts[0] + "?",
                "answer": parts[1].strip() if len(parts) > 1 else "N/A",
                "type": "short_answer"
            })
    return questions
