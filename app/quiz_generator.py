from transformers import pipeline

qa_model = pipeline("text2text-generation", model="iarfmoose/t5-base-question-generator")

def generate_quiz(text):
    inputs = f"generate questions: {text[:500]}"
    output = qa_model(inputs, max_length=256, do_sample=True)
    questions = output[0]["generated_text"].split("\n")
    return [q.strip("- ") for q in questions if q.strip()]
