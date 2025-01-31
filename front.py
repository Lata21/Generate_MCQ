import streamlit as st
import requests

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000/generate-mcqs/"

# Streamlit UI
st.title("MCQ Generator")

# File upload
uploaded_files = st.file_uploader(
    "Upload PDF or Text Files", type=["pdf", "txt"], accept_multiple_files=True
)

# Number of questions
num_questions = st.number_input(
    "Number of MCQs", min_value=1, max_value=20, value=5, step=1
)

# State variables
if "mcqs" not in st.session_state:
    st.session_state.mcqs = None
if "show_answers" not in st.session_state:
    st.session_state.show_answers = False

# Generate MCQs button
if st.button("Generate MCQs"):
    if uploaded_files:
        files = [("files", (file.name, file, file.type)) for file in uploaded_files]
        response = requests.post(
            BACKEND_URL,
            data={"num_questions": num_questions},
            files=files,
        )

        if response.status_code == 200:
            mcqs = response.json().get("mcqs", [])
            if mcqs:
                st.session_state.mcqs = mcqs
                st.session_state.show_answers = False
                st.success("MCQs generated successfully!")
            else:
                st.warning("No MCQs generated. Try providing more content.")
        else:
            st.error("Error generating MCQs. Check your input.")
    else:
        st.error("Please upload a file to generate MCQs.")

# Display MCQs
if st.session_state.mcqs:
    for i, mcq in enumerate(st.session_state.mcqs, start=1):
        st.markdown(f"### Question {i}:")
        st.write(mcq["question_stem"])
        for j, choice in enumerate(mcq["answer_choices"], start=1):
            st.write(f"{chr(64+j)}. {choice}")

    # Show Results button
    if st.button("Show Results"):
        st.session_state.show_answers = True

    # Display answers if the button is clicked
    if st.session_state.show_answers:
        st.markdown("### Answers:")
        for i, mcq in enumerate(st.session_state.mcqs, start=1):
            st.write(f"**Question {i} Correct Answer:** {mcq['correct_answer']}")
