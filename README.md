# Intern Live Build — Resume API + Grounded Support Agent

A small Flask application implementing both test tasks.

## 1. Setup

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Add the LLM API key

PowerShell:

```powershell
$env:OPENAI_API_KEY="YOUR_API_KEY"
```

Do not commit the API key to GitHub.

## 3. Run

```powershell
python app.py
```

Open:

http://127.0.0.1:5000

## API

Resume:

GET `/api/resume`

Chat:

POST `/api/chat`

Example JSON:

```json
{
  "messages": [
    {"role": "user", "content": "How much is deep cleaning?"},
    {"role": "assistant", "content": "Deep cleaning is ₹1,500 for a 1BHK, ₹2,000 for a 2BHK, and ₹2,500 for a 3BHK."},
    {"role": "user", "content": "And for a 3BHK?"}
  ]
}
```

## Test questions

Supported:
- How much is deep cleaning?
- And for a 3BHK?
- What areas do you cover?
- What time do you operate?
- What is the cancellation policy?

Should decline:
- What is the CEO's name?
- Can you book me a 3 PM slot tomorrow?
- What is the price of a service not in the knowledge base?

## What to say in the demo

"I chose Flask because it lets me build the API, page and chat endpoint quickly in one small project. I kept the resume as structured data and exposed it through GET /api/resume. For the support agent, I put the small knowledge base directly in the system prompt as requested. Temperature is zero and the prompt explicitly prevents unsupported answers. I also kept the last ten messages so the agent can handle multi-turn questions. I did not build authentication, RAG, embeddings, conversation storage or deployment because those were outside the minimum scope and would reduce the chance of finishing."
