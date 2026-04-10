from langchain_groq import ChatGroq
import os

# ✅ Initialize Groq
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

def run_agent(user_input):
    try:
        response = llm.invoke(user_input)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"
