from langchain_groq import ChatGroq
import os

# ✅ Updated working model
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

def run_agent(user_input):
    try:
        prompt = f"""
You are a friendly student assistant.

Explain the answer in a simple and clear way.

Rules:
- Use easy language
- Keep it short
- Use bullet points if needed
- Give 1 simple example

Question:
{user_input}
"""
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
