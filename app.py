import os
import time
import re
from typing import Tuple, Dict, Any

import streamlit as st
import pdfplumber
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

# --- Streamlit rerun compatibility ---
if not hasattr(st, "rerun"):  # fallback for old Streamlit versions
    st.rerun = st.experimental_rerun

# ------------- Config -------------
st.set_page_config(page_title="ATS Resume Screener", page_icon="🤖", layout="wide")
st.title("🤖 ATS Resume Screener")

# Read API key 
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
if not OPENAI_API_KEY:
    st.error("Missing OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ------------- Helpers -------------
def clean_text(t: str) -> str:
    """Basic cleanup to compress whitespace and strip control chars."""
    t = t.replace("\x00", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

def extract_pdf_text(uploaded_file) -> str:
    """Extract text from ALL pages using pdfplumber; fall back with friendly errors."""
    if uploaded_file is None:
        raise ValueError("No file uploaded.")
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            pages_text = []
            for p in pdf.pages:
                pages_text.append(p.extract_text() or "")
        text = "\n".join(pages_text)
        text = clean_text(text)
        if len(text) < 50:
            st.info(
                "The PDF seems mostly scanned or image-based. "
                "If text looks sparse, consider uploading a text-based PDF."
            )
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to read PDF: {e}")

def chunk_text(text: str, max_chars: int = 12000):
    """Yield chunks to keep prompts under token limits."""
    text = text.strip()
    for i in range(0, len(text), max_chars):
        yield text[i:i+max_chars]

def call_openai(messages, model: str, temperature: float = 0.2, max_tokens: int = 1000) -> str:
    """Thin wrapper with retry/backoff for OpenAI chat completions."""
    last_err = None
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"OpenAI API failed after retries: {last_err}")

# ------------- Prompts -------------
EVAL_SYSTEM = """You are a seasoned Technical Hiring Manager specializing in Data Science, ML/AI and MLOps.
Write clear, structured, evidence-based feedback grounded ONLY in the provided resume and job description.
Be concise but specific; avoid generic fluff. Use bullet points where helpful."""

EVAL_USER_TMPL = """JOB DESCRIPTION:
---
{jd}

RESUME:
---
{resume}

TASK:
Evaluate whether the candidate fits the JD. Provide:
1) Summary fit (2-3 sentences)
2) Strengths (bullet points with evidence)
3) Gaps/Risks (bullet points with evidence)
4) Role alignment (what seniority/track seems best)
5) Actionable suggestions to improve the resume for this JD"""

ATS_SYSTEM = """You are an expert ATS that understands DS/ML/AI roles and keyword matching.
Score strictly using the provided texts. No external assumptions."""

ATS_USER_TMPL = """JOB DESCRIPTION:
---
{jd}

RESUME:
---
{resume}

TASK:
1) Give a single percentage match (0-100). Be disciplined and justify briefly.
2) List missing critical keywords/skills from the JD that are not evidenced in the resume.
3) Final thoughts (1-3 bullets).

FORMAT:
- First line: "Match: XX%"
- Then: "Missing keywords:" as a comma-separated list
- Then: "Notes:" as 1-3 short bullets"""

# ------------- Sidebar (controls) -------------
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.selectbox(
        "Model",
        options=[
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4.1-mini",
            "gpt-4.1",
            "gpt-3.5-turbo",  
        ],
        index=0,
        help="Pick a model"
    )
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.05)
    max_tokens = st.slider("Max tokens in response", 256, 4096, 1200, 64)

# ------------- Main UI -------------
col1, col2 = st.columns([1.2, 1])

with col1:
    jd_text = st.text_area(
        "📄 Paste Job Description (JD)",
        height=220,
        placeholder="Paste the JD here…"
    )

with col2:
    uploaded_pdf = st.file_uploader(
        "📎 Upload Resume (PDF)",
        type=["pdf"],
        help="A text-based PDF works best. For image-only PDFs, try to re-export with selectable text."
    )
    if uploaded_pdf is not None:
        st.caption(f"Uploaded: **{uploaded_pdf.name}**")

st.markdown("---")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    run_eval = st.button("🧠 Tell me about the resume")
with c2:
    run_match = st.button("📊 Percentage match with JD")
with c3:
    clear_btn = st.button("🧹 Clear")

if clear_btn:
    try:
        st.cache_data.clear()
        st.cache_resource.clear()
    except Exception:
        pass
    st.session_state.clear()
    st.rerun()

# ------------- Actions -------------
def guard_inputs() -> Tuple[str, str]:
    if not OPENAI_API_KEY:
        st.error("OpenAI API key missing. Set `OPENAI_API_KEY` and re-run.")
        st.stop()
    if not jd_text or len(jd_text.strip()) < 15:
        st.error("Please paste a valid Job Description.")
        st.stop()
    if uploaded_pdf is None:
        st.error("Please upload a resume PDF.")
        st.stop()
    resume_text = extract_pdf_text(uploaded_pdf)
    if len(resume_text) < 20:
        st.error("Could not extract meaningful text from the PDF.")
        st.stop()
    return jd_text.strip(), resume_text

def run_resume_eval():
    jd, resume = guard_inputs()
    # If resume is huge, stream pieces to the model with a short “context building” step.
    chunks = list(chunk_text(resume, max_chars=12000))
    stitched_resume = ""
    for i, ch in enumerate(chunks, 1):
        stitched_resume += f"\n\n[RESUME_PART_{i}]\n{ch}"
    user_prompt = EVAL_USER_TMPL.format(jd=jd, resume=stitched_resume)
    with st.spinner("Analyzing resume vs JD…"):
        out = call_openai(
            messages=[
                {"role": "system", "content": EVAL_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            model=model, temperature=temperature, max_tokens=max_tokens
        )
    st.subheader("🧠 Evaluation")
    st.write(out)

def run_ats_match():
    jd, resume = guard_inputs()
    chunks = list(chunk_text(resume, max_chars=12000))
    stitched_resume = ""
    for i, ch in enumerate(chunks, 1):
        stitched_resume += f"\n\n[RESUME_PART_{i}]\n{ch}"
    user_prompt = ATS_USER_TMPL.format(jd=jd, resume=stitched_resume)
    with st.spinner("Computing ATS match…"):
        out = call_openai(
            messages=[
                {"role": "system", "content": ATS_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            model=model, temperature=0.0, max_tokens=max_tokens  # stricter scoring
        )
    # bold the Match line for readability
    first_line, *rest = out.splitlines()
    if first_line.strip().lower().startswith("match:"):
        st.subheader("📊 ATS Match")
        st.markdown(f"**{first_line.strip()}**")
        if rest:
            st.markdown("\n".join(rest))
    else:
        st.subheader("📊 ATS Match")
        st.write(out)

# Fire actions
if run_eval:
    run_resume_eval()
elif run_match:
    run_ats_match()