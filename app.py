from flask import Flask, jsonify, render_template, request
import os
from openai import OpenAI

app = Flask(__name__)

RESUME = {
    "profile": {
        "name": "Arram Ruchitha",
        "title": "B.Tech CSE (Data Science)",
        "email": "ruchiruchitha970@gmail.com",
        "phone": "+91 8919763272",
        "linkedin": "https://www.linkedin.com/in/arram-ruchitha-29a4b1281/",
        "github": "https://github.com/Ruchiruchitha29",
        "summary": "B.Tech Data Science graduate seeking Data Science / ML Engineering roles."
    },
    "education": [
        {"institution": "Sphoorthy Engineering College", "degree": "B.Tech CSE (Data Science)",
         "duration": "Nov 2022 - May 2026", "score": "8.01 CGPA"},
        {"institution": "Sri Gayatri Junior College", "degree": "Intermediate (MPC)",
         "duration": "Jun 2020 - May 2022", "score": "76%"}
    ],
    "experience": [
        {"company": "Tata Group (Forage)", "role": "GenAI Powered Data Analytics Job Simulation",
         "duration": "Jul 2026",
         "highlights": ["Ran EDA and built predictive models for financial delinquency risk.",
                        "Built a data-storytelling report and proposed an AI-driven collections strategy."]},
        {"company": "Google (AICTE & EduSkills)", "role": "Android Developer Virtual Internship",
         "duration": "Apr 2024 - Jun 2024",
         "highlights": ["Built native Android apps with Kotlin/Android Studio.",
                        "REST API integration, app lifecycle management, debugging."]},
        {"company": "Celonis (AICTE & EduSkills)", "role": "Process Mining Virtual Internship",
         "duration": "Jan 2024 - Mar 2024",
         "highlights": ["Analyzed enterprise process event logs, identified bottlenecks via KPIs.",
                        "Built interactive dashboards and process models."]}
    ],
    "projects": [
        {"title": "AI Fitness Trainer", "stack": "Python, OpenCV, MediaPipe",
         "description": "Real-time pose estimation app; automates squat rep counting via knee-angle calculation."},
        {"title": "Voice-Assisted Email Monitoring System", "stack": "Python, NLP, STT/TTS",
         "description": "Voice-controlled email client for visually impaired users."},
        {"title": "CareerCompass AI", "stack": "Python, Streamlit, ML",
         "description": "Placement prediction and ATS resume analyzer app."}
    ],
    "skills": ["Python", "SQL", "Kotlin", "TensorFlow", "PyTorch", "Matplotlib",
               "Seaborn", "Flask", "Git/GitHub", "Excel"]
}

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
10. Grocery delivery is available within the service areas and normally takes 60-90 minutes.
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