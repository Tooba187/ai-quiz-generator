from transformers import pipeline
import random

qa_model = pipeline("question-generation", model="iarfmoose/t5-base-question-generator")

def generate_quiz(text, num_questions=3):
    # Limit input to first 500 words to avoid model crash
    trimmed_text = " ".join(text.split()[:500])
    result = qa_model(trimmed_text)

    questions = []
    for item in result[:num_questions]:
        q = {"question": item["question"], "type": "short"}
        if item.get("answer"):
            q["type"] = "mcq"
            q["options"] = [item["answer"], "Option B", "Option C", "Option D"]
            random.shuffle(q["options"])
        questions.append(q)
    return questions
