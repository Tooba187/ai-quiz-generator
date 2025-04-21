from transformers import pipeline

qa_model = pipeline("text2text-generation", model="iarfmoose/t5-base-question-generator")

def generate_quiz(text, num_questions=3):
    chunks = text.strip().split(".")
    chunks = [c.strip() for c in chunks if len(c.strip()) > 20]
    selected = chunks[:num_questions]

    questions = []
    for chunk in selected:
        result = qa_model("generate question: " + chunk, max_length=64, do_sample=True)
        question = result[0]['generated_text']
        questions.append({
            "question": question,
            "type": "short"
        })
    return questions
