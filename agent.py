from langchain_groq import ChatGroq
import os
import re

# ✅ Initialize Groq LLM
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

# Store sessions
training_sessions = []

def run_agent(user_input):
    user_lower = user_input.lower()

    # 🎯 Greeting + Introduction
    if any(word in user_lower for word in ["hi", "hello", "hey"]):
        return """
Hey there! 👋

I'm your AI Training Assistant 🤖 (Student Helper Mode)

I can help you with:
📚 Explaining study concepts in simple terms  
📅 Scheduling training sessions  
📋 Viewing your sessions  
❌ Deleting sessions  
🧮 Performing calculations  
📊 Creating your weekly training plan  

Try:
👉 'What is machine learning?'  
👉 'schedule training monday 10am'  
👉 'plan my week'  

How can I help you today? 😊
"""

    # 🎯 Schedule training
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

        return f"Training scheduled on {day} at {time} ✅"

    # 🎯 Show sessions
    elif "show" in user_lower or "list" in user_lower:
        if training_sessions:
            response = "Here are your training sessions:\n\n"
            for i, session in enumerate(training_sessions, 1):
                response += f"{i}. {session['day'].title()} at {session['time']} → {session['details']}\n"
            return response
        else:
            return "No training sessions scheduled yet."

    # 🎯 Delete session
    elif "delete" in user_lower:
        if training_sessions:
            try:
                index = int(re.findall(r"\d+", user_lower)[0]) - 1
                removed = training_sessions.pop(index)
                return f"Removed session: {removed['details']} ❌"
            except:
                return "Please specify a valid session number to delete."
        else:
            return "No sessions to delete."

    # 🎯 Calculator
    elif "calculate" in user_lower:
        try:
            expression = user_lower.replace("calculate", "").strip()
            result = eval(expression)
            return f"The result is {result}"
        except:
            return "Please provide a valid calculation."

    # 🎯 Weekly Planner
    elif "plan my week" in user_lower or "weekly plan" in user_lower:
        if training_sessions:
            plan_text = ""
            for session in training_sessions:
                plan_text += f"{session['day']} at {session['time']}\n"

            prompt = f"""
You are a helpful study planner.

Generate a weekly training plan ONLY based on:

{plan_text}

Rules:
- Keep it short
- Only list days and time
- Add one motivational line
"""

            try:
                response = llm.invoke(prompt)
                return response.content
            except:
                return "⚠️ AI is busy, please try again."

        else:
            return "No training sessions found. Try scheduling some first!"

    # 🎯 Help
    elif "help" in user_lower:
        return """
📚 Ask study questions → 'What is AI?'
📅 Schedule → 'schedule training monday 10am'
📋 Show → 'show sessions'
❌ Delete → 'delete 1'
🧮 Calculate → 'calculate 5 + 3'
📊 Plan → 'plan my week'
"""

    # 🎯 Default AI (STUDENT MODE)
    else:
        try:
            prompt = f"""
You are a friendly student assistant.

Explain the answer in a simple and clear way.

Rules:
- Use easy language
- Give short explanation
- Use bullet points if needed
- Add example if helpful

Question:
{user_input}
"""
            response = llm.invoke(prompt)
            return response.content

        except:
            return "⚠️ AI is busy, please try again."
