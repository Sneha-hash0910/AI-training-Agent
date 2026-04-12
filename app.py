import streamlit as st
from PyPDF2 import PdfReader
from agent import run_agent

st.title("AI Training Assistant 🤖")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()

    st.success("PDF uploaded successfully!")

user_input = st.text_input("Ask something")

if user_input:
    if pdf_text:
        # 🔥 Ask from PDF
        full_input = f"""
Answer based on this document:

{pdf_text}

Question:
{user_input}
"""
        response = run_agent(full_input)
    else:
        response = run_agent(user_input)

    st.write(response)
