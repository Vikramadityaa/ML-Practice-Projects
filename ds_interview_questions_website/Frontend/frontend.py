import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8080"  # Change if your FastAPI is running on a different port

def ask_and_answer():

    # Topic selection dropdown
    topic = st.selectbox("Select a topic", ["Machine Learning", "Deep Learning", "Python"])

    if st.button("Get Questions"):
        response = requests.get(f"{API_BASE_URL}/questions?topic={topic}")  # Corrected endpoint URL
        if response.status_code == 200:
            st.sessio   n_state.questions = response.json()  # Store questions in session state
            st.session_state.user_answers = {q['id']: "" for q in st.session_state.questions}  # Initialize answers
        else:
            st.error("Failed to fetch questions. Please try again.")

    st.session_state.setdefault("questions", [])
    st.session_state.setdefault("user_answers", {})

    if st.session_state.questions:
        st.subheader("Answer the following questions:")

        for question in st.session_state.questions:
            st.write(f"**Q{question['id']}: {question['question_text']}**")
            st.session_state.user_answers[question['id']] = st.text_area(
                f"Your Answer for Q{question['id']}",
                key=f"answer_{question['id']}",
                value=st.session_state.user_answers.get(question['id'], "")
            )

        if st.button("Submit Answers"):
            results = []
            for question_id, answer in st.session_state.user_answers.items():
                response = requests.post(f"{API_BASE_URL}/submit_answer", json={
                    "user_id": 1,  # Placeholder for user ID
                    "question_id": question_id,
                    "answer_text": answer
                })
                if response.status_code == 200:
                    results.append(response.json())
                else:
                    st.error(f"Failed to evaluate answer for Q{question_id}.")

            st.subheader("Evaluation Results:")
            for i, result in enumerate(results):
                st.write(f"**Q{i + 1}: Score: {result['score']}, Suggested Answer: {result.get('correct_answer', 'N/A')}**")
