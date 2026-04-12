from langchain_groq import ChatGroq
import os
import re

# ✅ Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

training_sessions = []
chat_history = []

def detect_intent(user_input):
    prompt = f"""
Classify the user intent strictly into ONE of these words:

schedule
show
delete
calculate
plan
study

Only return one word from above. No extra text.

User input:
{user_input}
"""
    try:
        response = llm.invoke(prompt).content.lower().strip()

        # 🔥 extra safety
        if "schedule" in response:
            return "schedule"
        elif "show" in response:
            return "show"
        elif "delete" in response:
            return "delete"
        elif "calculate" in response:
            return "calculate"
        elif "plan" in response:
            return "plan"
        else:
            return "study"

    except:
        return "study"


def run_agent(user_input, training_sessions, chat_history):
    user_lower = user_input.lower().strip()

    chat_history.append(f"User: {user_input}")

    # 🎯 Greeting
    if user_lower in ["hi", "hello", "hey"]:
        response = """
Hey there! 👋

I'm your AI Training Assistant 🤖

I can:
📚 Answer study questions  
📅 Manage training schedules  
📋 Track sessions  
🧮 Do calculations  
📊 Create weekly plans  

Just talk normally — no strict commands needed 😊
"""
        chat_history.append(f"AI: {response}")
        return response

    # 🔥 AI decides intent
    intent = detect_intent(user_input)

    # 🎯 SCHEDULE (AI-assisted)
    if intent == "schedule":
        try:
            day_match = re.search(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", user_lower)
            time_match = re.search(r"\d{1,2}(am|pm)", user_lower)

            day = day_match.group() if day_match else "unspecified"
            time = time_match.group() if time_match else "unspecified"

            training_sessions.append({
                "day": day,
                "time": time,
                "details": user_input
            })

            response = f"✅ Scheduled on {day} at {time}"

        except:
            response = "⚠️ Could not schedule properly."

    # 🎯 SHOW
    elif intent == "show":
        if training_sessions:
            response = "📋 Your sessions:\n\n"
            for i, s in enumerate(training_sessions, 1):
                response += f"{i}. {s['day']} at {s['time']}\n"
        else:
            response = "❌ No sessions yet."

    # 🎯 DELETE
    elif intent == "delete":
        try:
            index = int(re.findall(r"\d+", user_lower)[0]) - 1
            removed = training_sessions.pop(index)
            response = f"❌ Removed: {removed['details']}"
        except:
            response = "⚠️ Mention valid session number."

    # 🎯 CALCULATE
    elif intent == "calculate":
        try:
            expression = re.sub(r"[^\d+\-*/().]", "", user_input)
            result = eval(expression)
            response = f"🧮 Result: {result}"
        except:
            response = "⚠️ Invalid calculation."

    # 🎯 PLAN
    elif intent == "plan" or "plan" in user_lower:
        if training_sessions:
            sessions_text = "\n".join([f"{s['day']} {s['time']}" for s in training_sessions])

            prompt = f"""
Create a weekly plan based on:

{sessions_text}

Keep it short + add motivation.
"""

            try:
                response = llm.invoke(prompt).content
            except:
                response = "⚠️ AI busy."
        else:
            response = "❌ No sessions to plan."

    # 🎯 STUDY / DEFAULT (FULL AI)
    else:
        try:
            context = "\n".join(chat_history[-5:])

            prompt = f"""
You are a intelligent, friendly and helpful student assistant.

Talk like a real human, not a robot.

Think before answering.

Guidelines:
-speak naturally like a human
- Use simple and natural language
- Be conversational and slightly friendly and helpful
- Adapt tone based on user question
- If user is confused → simplify more
- If user asks deep question → explain better
- Avoid repeating same style every time
- Only use bullet points if really needed
- Add a small friendly tone (like "let’s understand this" or "here’s a simple way to think about it")
-Do not repeat same sentence style every time
-Vary explanation style

Conversation:
{context}

User:
{user_input}

Answer:
"""

            response = llm.invoke(prompt).content

        except:
            response = "⚠️ AI busy, try again."

    chat_history.append(f"AI: {response}")
    return response
