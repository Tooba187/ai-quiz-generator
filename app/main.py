import streamlit as st
from file_parser import extract_text
from quiz_generator import generate_quiz

st.set_page_config(page_title="AI Quiz Generator", layout="centered")
st.title("AI Quiz Generator")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    text = extract_text(uploaded_file)
    if text:
        st.subheader("Extracted Content Preview:")
        st.text(text[:800])

        if st.button("Generate Quiz"):
            questions = generate_quiz(text, num_questions=3)
            st.subheader("Generated Quiz")
            for i, q in enumerate(questions, 1):
                st.markdown(f"**{i}. {q['question']}**")
                if q['type'] == "mcq":
                    st.radio("Options:", q['options'], key=i)
                else:
                    st.text_input("Answer:", key=i)
    else:
        st.error("Could not extract text from file.")
