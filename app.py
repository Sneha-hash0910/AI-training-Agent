import streamlit as st
from PyPDF2 import PdfReader
from agent import run_agent
from langchain_groq import ChatGroq
import os

# ✅ Groq LLM (for PDF mode)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

st.title("AI Training Assistant 🤖")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

pdf_text = ""

# ✅ Extract PDF
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        try:
            pdf_text += page.extract_text() or ""
        except:
            pass

    st.success("PDF uploaded successfully!")

user_input = st.text_input("Ask something")

# 🚀 MAIN LOGIC
if user_input:

    # 🔥 PDF MODE (direct AI, bypass agent)
    if pdf_text.strip():

        full_input = f"""
You are a friendly AI tutor.

Read the document carefully and explain the answer in simple words.

Rules:
- Speak like a human
- Keep it easy to understand
- Give example if helpful
- Do not mention "document"

Document:
{pdf_text[:5000]}

Question:
{user_input}
"""

        try:
            response = llm.invoke(full_input).content
        except:
            response = "⚠️ AI is busy, please try again."

    # 🎯 NORMAL MODE
    else:
        response = run_agent(user_input)

    st.write(response)
