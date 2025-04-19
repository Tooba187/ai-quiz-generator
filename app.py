import streamlit as st
from utils.file_processor import extract_text_from_file
from utils.quiz_generator import QuizGenerator
from utils.recommender import ResourceRecommender
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize components
quiz_gen = QuizGenerator()
recommender = ResourceRecommender()

# Pre-add some known good educational resources
known_resources = [
    "https://www.khanacademy.org/",
    "https://www.edx.org/learn/computer-science",
    "https://www.youtube.com/playlist?list=PLUl4u3cNGP63WbdFxL8giv4yhgdMGaZNA",
    "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/",
    "https://www.coursera.org/"
]

for resource in known_resources:
    recommender.add_resource(resource)

# Streamlit app
st.set_page_config(page_title="AI Quiz Generator", page_icon="📚", layout="wide")

def main():
    st.title("AI-Powered Personalized Quiz Generator")
    st.markdown("""
    Upload your study material (PDF, DOCX, or text) or enter a topic, and get a personalized quiz.
    After completing the quiz, you'll receive recommendations for learning resources to improve your weak areas.
    """)
    
    # Initialize session state
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    
    # Input options
    input_option = st.radio("Choose input method:", ("Upload a file", "Enter text directly"))
    
    content = ""
    if input_option == "Upload a file":
        uploaded_file = st.file_uploader("Upload your document (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
        if uploaded_file:
            content = extract_text_from_file(uploaded_file)
    else:
        content = st.text_area("Enter your study content or topic:", height=200)
    
    # Quiz generation controls
    if content:
        with st.expander("Quiz Settings"):
            col1, col2 = st.columns(2)
            with col1:
                num_questions = st.slider("Number of questions", 3, 20, 10)
            with col2:
                question_types = st.multiselect(
                    "Question types",
                    ["multiple_choice", "true_false", "short_answer"],
                    ["multiple_choice", "true_false"]
                )
        
        if st.button("Generate Quiz"):
            with st.spinner("Generating quiz questions..."):
                quiz_data = quiz_gen.generate_quiz(content, num_questions, question_types)
                st.session_state.quiz_data = quiz_data
                st.session_state.user_answers = {}
                st.session_state.quiz_submitted = False
                st.success("Quiz generated successfully!")
    
    # Display quiz if available
    if st.session_state.quiz_data and 'quiz' in st.session_state.quiz_data:
        st.header("Generated Quiz")
        
        if 'error' in st.session_state.quiz_data:
            st.error(st.session_state.quiz_data['error'])
        else:
            with st.form("quiz_form"):
                for i, question in enumerate(st.session_state.quiz_data['quiz']):
                    st.subheader(f"Question {i+1}")
                    st.write(question['question'])
                    
                    if question['type'] == 'multiple_choice':
                        options = question['options']
                        st.session_state.user_answers[i] = st.radio(
                            f"Options for question {i+1}",
                            options,
                            key=f"q_{i}",
                            index=None
                        )
                    elif question['type'] == 'true_false':
                        st.session_state.user_answers[i] = st.radio(
                            f"True or False for question {i+1}",
                            ["True", "False"],
                            key=f"q_{i}",
                            index=None
                        )
                    else:  # short_answer
                        st.session_state.user_answers[i] = st.text_input(
                            f"Your answer for question {i+1}",
                            key=f"q_{i}"
                        )
                    
                    st.divider()
                
                submitted = st.form_submit_button("Submit Quiz")
                if submitted:
                    st.session_state.quiz_submitted = True
            
            # Show results and recommendations after submission
            if st.session_state.quiz_submitted:
                st.header("Quiz Results")
                score = 0
                weak_topics = set()
                
                for i, question in enumerate(st.session_state.quiz_data['quiz']):
                    user_answer = st.session_state.user_answers.get(i, "")
                    correct_answer = str(question['answer']).strip().lower()
                    
                    st.subheader(f"Question {i+1}")
                    st.write(question['question'])
                    
                    if question['type'] == 'multiple_choice':
                        if user_answer and user_answer.strip().lower() == correct_answer:
                            score += 1
                            st.success(f"✅ Correct! Your answer: {user_answer}")
                        else:
                            st.error(f"❌ Incorrect. Your answer: {user_answer or 'Empty'}. Correct answer: {correct_answer}")
                            weak_topics.update(st.session_state.quiz_data.get('topics_covered', []))
                    elif question['type'] == 'true_false':
                        if user_answer and user_answer.strip().lower() == correct_answer:
                            score += 1
                            st.success(f"✅ Correct! Your answer: {user_answer}")
                        else:
                            st.error(f"❌ Incorrect. Your answer: {user_answer or 'Empty'}. Correct answer: {correct_answer}")
                            weak_topics.update(st.session_state.quiz_data.get('topics_covered', []))
                    else:  # short_answer
                        st.write(f"Your answer: {user_answer or 'Empty'}")
                        st.info(f"Sample correct answer: {correct_answer}")
                        # For short answers, we don't automatically score
                
                # Calculate and display score
                total_questions = len(st.session_state.quiz_data['quiz'])
                if total_questions > 0:
                    percentage = (score / total_questions) * 100
                    st.metric("Your Score", f"{score}/{total_questions} ({percentage:.1f}%)")
                
                # Show recommendations for weak areas
                if weak_topics:
                    st.header("Recommended Learning Resources")
                    st.info("Here are some resources to help you improve in areas where you struggled:")
                    
                    for topic in weak_topics:
                        st.subheader(f"Resources for: {topic}")
                        resources = recommender.recommend_resources(topic, num_recommendations=2)
                        
                        if resources:
                            for resource in resources:
                                st.markdown(f"- [{resource}]({resource})")
                        else:
                            st.warning("No specific resources found. Try searching online for this topic.")

if __name__ == "__main__":
    main()
