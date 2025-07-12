# app/main.py

import streamlit as st
from backend import process_user_message, generate_notes, generate_question_paper
from utils import get_file_bytesio

st.set_page_config(page_title="AI Study Assistant", page_icon=":robot_face:", layout="wide")

# Sidebar settings
st.sidebar.title("Settings")
difficulty = st.sidebar.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
export_format = st.sidebar.radio("Export Format", ["PDF", "Word"])
language = st.sidebar.selectbox("Language", ["English (US)", "Hindi", "Spanish"])

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

st.title("🤖 AI Study Assistant")

# File upload
st.markdown("#### Upload Documents")
uploaded_files = st.file_uploader(
    "Upload PDFs, Word docs, or text files", 
    type=["pdf", "docx", "txt"], 
    accept_multiple_files=True
)
if uploaded_files:
    st.session_state.uploaded_files = uploaded_files

# Chat area
st.markdown("#### Chat")
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

user_input = st.chat_input("Type your message and press Enter...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare files for backend
    files_to_process = get_file_bytesio(st.session_state.uploaded_files) if st.session_state.uploaded_files else None

    with st.spinner("AI is typing..."):
        ai_reply = process_user_message(
            user_input, 
            files=files_to_process, 
            audio=None,
            difficulty=difficulty,
            language=language
        )
    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.markdown(ai_reply)

# Action buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Generate Notes"):
        files_to_process = get_file_bytesio(st.session_state.uploaded_files) if st.session_state.uploaded_files else None
        with st.spinner("Generating notes..."):
            notes = generate_notes(files_to_process, difficulty)
            st.success("Notes generated!")
            st.download_button("Download Notes", notes, file_name="notes.pdf" if export_format=="PDF" else "notes.docx")
with col2:
    if st.button("Create Question Paper"):
        files_to_process = get_file_bytesio(st.session_state.uploaded_files) if st.session_state.uploaded_files else None
        with st.spinner("Creating question paper..."):
            questions = generate_question_paper(files_to_process, difficulty)
            st.success("Question paper ready!")
            st.download_button("Download Questions", questions, file_name="questions.pdf" if export_format=="PDF" else "questions.docx")

# Instructions
with st.expander("ℹ️ How to use this app"):
    st.markdown("""
    - **Upload** your study materials (PDF, Word, or text files).
    - **Chat** with the AI using the chat box below.
    - **Generate notes** or a **question paper** using the buttons.
    - **Download** your results in PDF or Word format.
    """)
