import streamlit as st
from PyPDF2 import PdfReader
from agent import run_agent

st.set_page_config(page_title="AI Training Assistant", page_icon="🤖")

st.title("AI Training Assistant 🤖")

# 🔥 FIX: Store sessions & memory in Streamlit
if "training_sessions" not in st.session_state:
    st.session_state.training_sessions = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 📄 PDF Upload
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text

    st.success("PDF uploaded successfully!")

# 💬 User Input
user_input = st.text_input("Ask something")

# 🚀 Handle Input
if user_input:

    # 🔥 Pass session + memory to agent
    if pdf_text:
        full_input = f"""
Answer based on this document:

{pdf_text}

Question:
{user_input}
"""
        response = run_agent(
            full_input,
            st.session_state.training_sessions,
            st.session_state.chat_history
        )
    else:
        response = run_agent(
            user_input,
            st.session_state.training_sessions,
            st.session_state.chat_history
        )

    st.write(response)
