from langchain_groq import ChatGroq
import os
import re
import time

# ✅ Initialize Groq LLM
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

training_sessions = []

def ask_ai(prompt):
    """Retry mechanism for Groq"""
    try:
        response = llm.invoke(prompt)
        return response.content
    except:
        try:
            time.sleep(2)  # wait and retry
            response = llm.invoke(prompt)
            return response.content
        except:
            return "⚠️ AI is busy right now. Please try again in a few seconds."

def run_agent(user_input):
    user_lower = user_input.lower().strip()

    # 🎯 Greeting (FIXED)
    if user_lower in ["hi", "hello", "hey"]:
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

    # 🎯 Schedule
    elif "schedule" in user_lower:
        day_match = re.search(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", user_lower)
        time_match = re.search(r"\d{1,2}(am|pm)", user_lower)

        day = day_match.group() if day_match else "unspecified day"
        time = time_match.group() if time_match else "unspecified time"

        training_sessions.append({
            "day": day,
            "time": time,
            "details": user_input
        })

        return f"Training scheduled on {day} at {time} ✅"

    # 🎯 Show
    elif "show" in user_lower or "list" in user_lower:
        if training_sessions:
            return "\n".join([
                f"{i+1}. {s['day'].title()} at {s['time']} → {s['details']}"
                for i, s in enumerate(training_sessions)
            ])
        return "No training sessions scheduled yet."

    # 🎯 Delete
    elif "delete" in user_lower:
        if training_sessions:
            try:
                index = int(re.findall(r"\d+", user_lower)[0]) - 1
                removed = training_sessions.pop(index)
                return f"Removed: {removed['details']} ❌"
            except:
                return "Please provide valid session number."
        return "No sessions to delete."

    # 🎯 Calculator
    elif "calculate" in user_lower:
        try:
            expression = user_lower.replace("calculate", "").strip()
            return f"Result: {eval(expression)}"
        except:
            return "Invalid calculation."

    # 🎯 Weekly Plan
    elif "plan my week" in user_lower or "weekly plan" in user_lower:
        if training_sessions:
            plan_text = "\n".join([f"{s['day']} at {s['time']}" for s in training_sessions])

            prompt = f"""
Create a simple weekly training plan based on:

{plan_text}

Keep it short and add one motivational line.
"""
            return ask_ai(prompt)
        return "No sessions found."

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

    # 🎯 DEFAULT (REAL AI)
    else:
        prompt = f"""
You are a friendly student assistant.

Explain clearly and simply.

- Use easy language
- Keep it short
- Use bullet points if needed
- Give 1 example

Question:
{user_input}
"""
        return ask_ai(prompt)
