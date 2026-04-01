import streamlit as st
from agent import run_agent

st.title("🎓 Student AI Assistant")

user_input = st.text_input("Ask your question:")

if user_input:
    response = run_agent(user_input)
    st.write(response)
