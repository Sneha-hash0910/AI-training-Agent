from langchain_openai import ChatOpenAI
import os
import re

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# Store sessions
training_sessions = []

def run_agent(user_input):
    user_lower = user_input.lower()

    # 🎯 Schedule training
    if "schedule" in user_lower:
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

    # 🎯 Weekly Planner (AI)
    elif "plan my week" in user_lower or "weekly plan" in user_lower:
        if training_sessions:
            plan_text = ""
            for session in training_sessions:
                plan_text += f"{session['day']} at {session['time']}\n"

            prompt = f"""
You are a training assistant.

Generate a weekly training plan ONLY based on the sessions below.

Sessions:
{plan_text}

Rules:
- Keep it short and clear
- Only list days and time
- Add 1 short motivational line at the end
"""

            response = llm.invoke(prompt)
            return response.content

        else:
            return "No training sessions found. Try scheduling some first!"

    # 🎯 Help
    elif "help" in user_lower:
        return """
📅 Schedule → 'schedule training monday 10am'
📋 Show → 'show sessions'
❌ Delete → 'delete 1'
🧮 Calculate → 'calculate 5 + 3'
📊 Plan → 'plan my week'
"""

    # 🎯 Default AI response
    else:
        response = llm.invoke(user_input)
        return response.content
