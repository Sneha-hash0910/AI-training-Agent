import streamlit as st
from PyPDF2 import PdfReader
from agent import run_agent

st.title("AI Training Assistant 🤖")

# ✅ Session state for memory
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "training_sessions" not in st.session_state:
    st.session_state.training_sessions = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 📄 Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# ✅ Extract PDF text
if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    pdf_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text

    st.session_state.pdf_text = pdf_text
    st.success("✅ PDF uploaded successfully!")

# ❌ Clear PDF button
if st.button("Clear PDF"):
    st.session_state.pdf_text = ""
    st.success("PDF cleared!")

# 💬 User input
user_input = st.text_input("Ask something")

if user_input:
    # ✅ If PDF exists → use it
    if st.session_state.pdf_text:
        full_input = f"""
Answer based on this document:

{st.session_state.pdf_text[:3000]}

Question:
{user_input}
"""
        response = run_agent(
            full_input,
            st.session_state.training_sessions,
            st.session_state.chat_history
        )

    # ✅ Normal query
    else:
        response = run_agent(
            user_input,
            st.session_state.training_sessions,
            st.session_state.chat_history
        )

    st.write(response)
