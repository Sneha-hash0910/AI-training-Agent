import streamlit as st
from agent import run_agent

st.set_page_config(page_title="AI Training Assistant", page_icon="🤖")

st.title("🤖 AI Training Assistant")

user_input = st.text_input("Ask something:")

if user_input:
    response = run_agent(user_input)
    st.write(response)
