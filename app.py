"""
FastAPI demo for the Lead Qualification Agent.

Run (after installing requirements):
    uvicorn app:app --reload

Try:
    POST /score
    {
      "company": "Bright Homes Realty",
      "industry": "Real Estate",
      "city": "Austin",
      "state": "TX",
      "email": "hello@brighthomes.example",
      "phone": "512-555-0100",
      "website": "https://brighthomes.example"
    }

This file is optional for the portfolio demo. The core logic lives in
agent.py and works with plain Python, no server needed.
"""

from agent import draft_outreach, score_lead

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except ImportError:  # pragma: no cover
    FastAPI = None
    BaseModel = object


if FastAPI is None:
    raise SystemExit("Install requirements first: pip install -r requirements.txt")

app = FastAPI(title="Lead Qualification Agent")


class Lead(BaseModel):
    company: str = ""
    industry: str = ""
    city: str = ""
    state: str = ""
    email: str = ""
    phone: str = ""
    website: str = ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/score")
def score(lead: Lead):
    data = lead.model_dump()
    score_value, grade, reasons = score_lead(data)
    return {
        "company": data["company"],
        "score": score_value,
        "grade": grade,
        "reasons": reasons,
        "outreach_draft": draft_outreach(data) if score_value >= 60 else "",
    }
