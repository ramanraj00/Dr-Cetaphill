from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS (for frontend running separately)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hackathon demo mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Report(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "Dr CetaPhill Backend Running 🚀"}

@app.post("/analyze")
async def analyze_report(report: Report):

    if not report.text.strip():
        return {"analysis": "⚠ No medical data provided."}

    prompt = f"""
You are Doctor CetaPhill, a friendly health report reader.

Explain lab results in PLAIN, SIMPLE ENGLISH like a caring doctor.
Never diagnose. Use phrases like "may suggest" or "could mean".
Keep explanations short and clear.

Use EXACTLY this format:

# 👤 Health Report
**Overall Health:** [🟢 Looking Good! | 🟡 A Few Things to Watch | 🔴 Needs Attention Soon]

---

## 📋 Quick Summary
2-3 simple sentences.

---

## 🔬 Abnormal Values
- List abnormal results in bullet points.

---

## ⚠ Risk Level
Explain overall risk in 2-3 lines.

---

## ✅ Suggestions
- Lifestyle
- Diet
- Exercise
- Doctor visit advice

---

Medical Report:
{report.text}
"""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 800,
                        "temperature": 0.2
                    }
                }
            )

        response.raise_for_status()
        result = response.json()

        return {"analysis": result.get("response", "⚠ Model returned empty response.")}

    except httpx.RequestError:
        return {"analysis": "⚠ Ollama is not running. Start it using: `ollama run phi3`"}

    except Exception as e:
        return {"analysis": f"⚠ Backend error: {str(e)}"}