import streamlit as st
from file_parser import extract_text
from quiz_generator import generate_quiz

st.set_page_config(page_title="AI Quiz Generator", layout="centered")
st.title("AI Quiz Generator")

uploaded_file = st.file_uploader("Upload a learning document (PDF or DOCX):", type=["pdf", "docx"])

if uploaded_file:
    text = extract_text(uploaded_file)
    if not text:
        st.error("Failed to extract content from the file.")
    else:
        st.subheader("Extracted Content Preview:")
        st.text(text[:1000])  # Preview only first 1000 chars

        if st.button("Generate Quiz"):
            quiz = generate_quiz(text, num_questions=3)
            st.subheader("Generated Quiz:")
            for i, q in enumerate(quiz, 1):
                st.markdown(f"**{i}. {q['question']}**")
                if q["type"] == "mcq":
                    st.radio("Choose one:", q["options"], key=f"q{i}")
                elif q["type"] == "short":
                    st.text_input("Your answer:", key=f"q{i}")
