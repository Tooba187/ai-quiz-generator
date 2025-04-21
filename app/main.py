import streamlit as st
from file_parser import extract_text
from quiz_generator import generate_quiz


st.set_page_config(page_title="AI Quiz Generator", layout="centered")
st.title("AI Quiz Generator")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    text = extract_text(uploaded_file)
    if not text:
        st.error("Could not extract any text.")
    else:
        st.subheader("Preview:")
        st.write(text[:800])

        if st.button("Generate Quiz"):
            questions = generate_quiz(text)
            for i, q in enumerate(questions, 1):
                st.markdown(f"**{i}. {q}**")

