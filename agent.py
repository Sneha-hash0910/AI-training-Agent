from langchain_groq import ChatGroq
import os
import re

# ✅ Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

# 📅 Store training sessions
training_sessions = []

# 🧠 Store conversation memory
chat_history = []

def run_agent(user_input):
    user_lower = user_input.lower().strip()

    # 🔹 Save user message to memory
    chat_history.append(f"User: {user_input}")

    # 🎯 Greeting
    if user_lower in ["hi", "hello", "hey"]:
        response = """
Hey there! 👋

I'm your AI Training Assistant 🤖 (Student Helper Mode)

I can help you with:
📚 Study concepts  
📅 Schedule training  
📋 Show sessions  
❌ Delete sessions  
🧮 Calculations  
📊 Weekly plan  

How can I help you today? 😊
"""
        chat_history.append(f"AI: {response}")
        return response

    # 🎯 Schedule
    elif "schedule" in user_lower:
        day_match = re.search(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", user_lower)
        time_match = re.search(r"\d{1,2}(am|pm)", user_lower)

        day = day_match.group() if day_match else "unspecified day"
        time = time_match.group() if time_match else "unspecified time"

        session = {
            "day": day,
            "time": time,
            "details": user_input
        }

        training_sessions.append(session)

        response = f"✅ Training scheduled on {day} at {time}"
        chat_history.append(f"AI: {response}")
        return response

    # 🎯 Show sessions
    elif "show" in user_lower or "list" in user_lower:
        if training_sessions:
            response = "📋 Your training sessions:\n\n"
            for i, session in enumerate(training_sessions, 1):
                response += f"{i}. {session['day'].title()} at {session['time']} → {session['details']}\n"
        else:
            response = "❌ No training sessions yet."

        chat_history.append(f"AI: {response}")
        return response

    # 🎯 Delete
    elif "delete" in user_lower:
        if training_sessions:
            try:
                index = int(re.findall(r"\d+", user_lower)[0]) - 1
                removed = training_sessions.pop(index)
                response = f"❌ Removed: {removed['details']}"
            except:
                response = "⚠️ Use: delete 1"
        else:
            response = "❌ No sessions to delete."

        chat_history.append(f"AI: {response}")
        return response

    # 🎯 Calculator
    elif "calculate" in user_lower:
        try:
            expression = user_lower.replace("calculate", "").strip()
            result = eval(expression)
            response = f"🧮 Result: {result}"
        except:
            response = "⚠️ Invalid calculation."

        chat_history.append(f"AI: {response}")
        return response

    # 🎯 Weekly plan (AI)
    elif "plan my week" in user_lower:
        if training_sessions:
            plan_text = "\n".join([f"{s['day']} at {s['time']}" for s in training_sessions])

            prompt = f"""
You are a student planner.

Sessions:
{plan_text}

Create a weekly plan.
Keep it short + add 1 motivational line.
"""

            try:
                response = llm.invoke(prompt).content
            except:
                response = "⚠️ AI busy, try again."

        else:
            response = "❌ No sessions found."

        chat_history.append(f"AI: {response}")
        return response

    # 🎯 Default → STUDY MODE WITH MEMORY
    else:
        try:
            # 🔥 Include past conversation (last 5 messages)
            context = "\n".join(chat_history[-5:])

            prompt = f"""
You are a friendly student assistant.

Conversation history:
{context}

Now answer the latest question clearly.

Rules:
- Simple language
- Short answer
- Bullet points if needed
- One example

Question:
{user_input}
"""

            response = llm.invoke(prompt).content

        except:
            response = "⚠️ AI is busy, please try again."

        chat_history.append(f"AI: {response}")
        return response
