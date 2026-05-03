import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document

load_dotenv()

# -------------------- STATE --------------------
class State(TypedDict):
    resume: str
    analysis: str
    feedback: str
    count: int

# -------------------- LLM --------------------
llm = ChatOpenAI(model="gpt-4o-mini")

# -------------------- NODES --------------------
def analyse_resume(state):
    prompt = f"""
    Analyse the following resume and provide detailed improvement suggestions:

    Focus on:
    - Skills
    - Experience
    - Projects
    - Structure
    - Impact 

    Resume:
    {state['resume']}

    Give atleast 5 strong, actionable suggestions for improvement.
    """

    if state["feedback"]:
        prompt += f"\n\nPrevious Feedback: {state['feedback']}"

    response = llm.invoke(prompt)

    return {
        "analysis": response.content,
        "count": state["count"] + 1
    }

def review_analysis(state):
    text = state["analysis"]

    if len(text) < 200:
        return {"feedback": "Too Short, add more details."}

    if "skills" not in text.lower():
        return {"feedback": "Missing skills section."}

    return {"feedback": "good"}

def should_continue(state):
    if state["feedback"] == "good" or state["count"] >= 3:
        return "end"
    return "retry"

# -------------------- GRAPH --------------------
builder = StateGraph(State)

builder.add_node("analyse", analyse_resume)
builder.add_node("review", review_analysis)

builder.add_edge(START, "analyse")
builder.add_edge("analyse", "review")

builder.add_conditional_edges(
    "review",
    should_continue,
    {
        "end": END,
        "retry": "analyse"
    }
)

graph = builder.compile()

# -------------------- UI DESIGN --------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide", page_icon="🤖")

# Custom CSS (🔥 Glassmorphism UI)
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

.main {
    background: transparent;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}

.title {
    font-size: 42px;
    font-weight: 700;
    color: white;
}

.subtitle {
    color: #cbd5e1;
}

.success-box {
    background: rgba(34,197,94,0.2);
    padding: 15px;
    border-radius: 10px;
}

.warning-box {
    background: rgba(239,68,68,0.2);
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="title">🤖 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">LangGraph + LLM powered smart resume feedback system</div>', unsafe_allow_html=True)

st.write("")

# -------------------- FILE UPLOAD --------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📂 Upload your Resume",
    type=["pdf", "docx", "txt"]
)

resume_text = ""

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        resume_text = text

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        text = [para.text for para in doc.paragraphs]
        resume_text = "\n".join(text)

    elif uploaded_file.type == "text/plain":
        resume_text = uploaded_file.read().decode("utf-8")

    st.markdown('<div class="success-box">✅ Resume uploaded successfully!</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- BUTTON --------------------
col1, col2 = st.columns([1,1])

with col1:
    analyze_btn = st.button("🚀 Analyze Resume", use_container_width=True)

# -------------------- ANALYSIS --------------------
if analyze_btn:
    if not resume_text.strip():
        st.markdown('<div class="warning-box">⚠️ Please upload a resume first.</div>', unsafe_allow_html=True)
    else:
        progress = st.progress(0)

        with st.spinner("Analyzing your resume..."):
            progress.progress(30)

            result = graph.invoke({
                "resume": resume_text,
                "analysis": "",
                "feedback": "",
                "count": 0
            })

            progress.progress(100)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("✨ Improvement Suggestions")
        st.write(result["analysis"])

        st.markdown("---")

        st.subheader("📊 Attempts Used")
        st.metric(label="Iterations", value=result["count"])

        st.markdown('</div>', unsafe_allow_html=True)
