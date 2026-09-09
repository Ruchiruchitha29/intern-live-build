from flask import Flask, jsonify, render_template, request
import os
from openai import OpenAI

app = Flask(__name__)

# -----------------------------
# Task 1: structured resume data
# -----------------------------
RESUME = {
    "profile": {
        "name": "ARRAM RUCHITHA",
        "title": "B.Tech Computer Science Engineering (Data Science)",
        "summary": "Fresher with a foundation in Python, SQL, data analysis and machine learning."
    },
    "experience": [
        {
            "company": "CloudVex Technologies",
            "role": "AI/ML Intern",
            "duration": "2026",
            "highlights": [
                "Worked on AI/ML application tasks.",
                "Built and improved application features."
            ]
        }
    ],
    "skills": ["Python", "SQL", "Machine Learning", "Data Analysis", "HTML", "CSS"]
}

# -----------------------------
# Task 2: grounded knowledge base
# -----------------------------
KB = """
Home Services Knowledge Base

1. Services: cleaning, pest control, laundry, plumbing, electrical and grocery delivery.
2. Deep cleaning price: ₹1,500 for a 1BHK, ₹2,000 for a 2BHK, and ₹2,500 for a 3BHK.
3. Regular cleaning price: ₹700 for a 1BHK, ₹900 for a 2BHK, and ₹1,100 for a 3BHK.
4. Pest control starts at ₹999.
5. Laundry pickup and delivery is available from 9 AM to 7 PM.
6. Home service operating hours are 8 AM to 8 PM.
7. Service areas: Hyderabad, Secunderabad and Gachibowli.
8. Same-day service is available when a slot is open.
9. Cancellations are free if made at least 2 hours before the scheduled service.
10. Grocery delivery is available within the service areas and normally takes 60–90 minutes.
"""

SYSTEM_PROMPT = f"""
You are a support agent for a home services business.

You MUST follow these rules:
- Answer ONLY using facts in the knowledge base below.
- If the answer is not supported by the knowledge base, say:
  "I don't know based on the information I have."
- Do not invent prices, timings, locations, policies, availability or other facts.
- Remember earlier messages in the conversation and use them when relevant.
- Be concise and helpful.

Knowledge base:
{KB}
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/api/resume")
def get_resume():
    return jsonify(RESUME)

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({
            "answer": "LLM API key is not configured. Set OPENAI_API_KEY and restart the app."
        }), 500

    client = OpenAI(api_key=api_key)

    safe_messages = []
    for message in messages[-10:]:
        role = message.get("role")
        content = message.get("content", "")
        if role in ("user", "assistant") and content:
            safe_messages.append({"role": role, "content": content})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *safe_messages
            ],
            temperature=0
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"LLM request failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
