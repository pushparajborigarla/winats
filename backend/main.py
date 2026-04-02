from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from ats_engine import calculate_ats
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/analyze")
async def analyze(resume: str = Form(...), jd: str = Form(...)):
    return calculate_ats(resume, jd)

@app.post("/chat")
async def chat(resume: str = Form(...), jd: str = Form(...), question: str = Form(...)):
    prompt = f"""Answer ONLY from resume and JD. Max 2 lines.

Resume:
{resume}

JD:
{jd}

Question:
{question}"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Strict ATS assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return {"answer": res.choices[0].message.content}
