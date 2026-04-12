from langchain_groq import ChatGroq
import os
import re
import ast
import operator

# ✅ Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

# 🔒 Safe calculator
def safe_eval(expr):
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    def eval_node(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return allowed_ops[type(node.op)](eval_node(node.left), eval_node(node.right))
        else:
            raise ValueError("Invalid expression")

    return eval_node(ast.parse(expr, mode='eval').body)


# 🧠 Intent detection using AI
def detect_intent(user_input):
    prompt = f"""
Classify the user intent into ONE word only:

schedule
show
delete
calculate
plan
study

Only return one word.

User input:
{user_input}
"""
    try:
        response = llm.invoke(prompt).content.lower().strip()

        if response in ["schedule", "show", "delete", "calculate", "plan"]:
            return response
        return "study"

    except:
        return "study"


# 🚀 MAIN AGENT
def run_agent(user_input, training_sessions, chat_history):
    user_lower = user_input.lower().strip()

    # Save user input
    chat_history.append(f"User: {user_input}")

    # 🎯 Greeting
    if user_lower in ["hi", "hello", "hey"]:
        response = """
Hey there! 👋

I'm your AI Training Assistant 🤖

I can:
📚 Answer study questions  
📅 Manage schedules  
📋 Track sessions  
🧮 Do calculations  
📊 Plan your week  

Just talk naturally 😊
"""
        chat_history.append(f"AI: {response}")
        return response

    # 🔥 Detect intent
    intent = detect_intent(user_input)

    # =========================
    # 📅 SCHEDULE
    # =========================
    if intent == "schedule":
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

    # =========================
    # 📋 SHOW
    # =========================
    elif intent == "show":
        if training_sessions:
            response = "📋 Your sessions:\n\n"
            for i, s in enumerate(training_sessions, 1):
                response += f"{i}. {s['day'].title()} at {s['time']}\n"
        else:
            response = "❌ No sessions yet."

    # =========================
    # ❌ DELETE
    # =========================
    elif intent == "delete":
        try:
            index = int(re.findall(r"\d+", user_lower)[0]) - 1
            removed = training_sessions.pop(index)
            response = f"❌ Removed: {removed['details']}"
        except:
            response = "⚠️ Please mention a valid session number (e.g., delete 1)"

    # =========================
    # 🧮 CALCULATE
    # =========================
    elif intent == "calculate":
        try:
            expression = re.sub(r"[^\d+\-*/().]", "", user_input)
            result = safe_eval(expression)
            response = f"🧮 Result: {result}"
        except:
            response = "⚠️ Invalid calculation."

    # =========================
    # 📊 PLAN
    # =========================
    elif intent == "plan":
        if training_sessions:
            sessions_text = "\n".join([f"{s['day']} at {s['time']}" for s in training_sessions])

            prompt = f"""
Create a weekly plan based on:

{sessions_text}

Rules:
- Keep it short
- Clear format
- Add one motivational line
"""

            try:
                response = llm.invoke(prompt).content
            except:
                response = "⚠️ AI is busy, try again."

        else:
            response = "❌ No sessions to plan."

    # =========================
    # 📚 STUDY MODE (REAL AI)
    # =========================
    else:
        try:
            context = "\n".join(chat_history[-5:])

            prompt = f"""
You are a smart, friendly student assistant.

Talk like a real human.

Guidelines:
- Keep it simple and clear
- Be slightly conversational
- Explain like a friend teaching
- Use examples if helpful
- Avoid robotic tone

Conversation:
{context}

User:
{user_input}

Answer:
"""

            response = llm.invoke(prompt).content

        except:
            response = "⚠️ AI is busy, try again."

    # Save response
    chat_history.append(f"AI: {response}")

    return response
