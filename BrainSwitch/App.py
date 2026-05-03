import streamlit as st
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import re
from langchain_community.tools import DuckDuckGoSearchRun

# ---- LOAD ENV ----
load_dotenv()

# ---- LLM ----
llm = ChatOpenAI(model="gpt-4o")

# ---- TOOLS ----
search_tool = DuckDuckGoSearchRun()

# ---- STATE ----
class AgentState(TypedDict):
    query: str
    decision: str
    tool_output: str
    final_answer: str

# ---- MEMORY INIT ----
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = []  # long-term memory

# ---- SAFE CALCULATOR ----
def safe_calculate(expression):
    try:
        if not re.match(r'^[0-9+\-*/(). ]+$', expression):
            return "⚠️ Invalid expression"
        return str(eval(expression, {"__builtins__": None}, {}))
    except:
        return "⚠️ Calculation error"

def calculator_tool(state):
    return {"tool_output": safe_calculate(state["query"])}

# ---- WEB SEARCH ----
def web_search_tool(state):
    try:
        result = search_tool.run(state["query"])
        return {"tool_output": result[:1000]}
    except:
        return {"tool_output": "⚠️ Web search failed"}

# ---- DECISION ----
def decide_action(state):
    query = state["query"].lower().strip()

    if re.match(r'^[0-9+\-*/(). ]+$', query):
        return {"decision": "calculator"}

    web_keywords = ["latest", "news", "today", "current", "price", "update"]
    if any(word in query for word in web_keywords):
        return {"decision": "web"}

    return {"decision": "answer"}

# ---- MEMORY EXTRACTOR ----
def update_memory(user_query, ai_response):
    prompt = f"""
    Extract important long-term facts from this conversation.
    Ignore casual talk.

    User: {user_query}
    AI: {ai_response}

    Return short bullet points.
    """

    memory = llm.invoke(prompt).content

    # store only meaningful memory
    if len(memory) > 10:
        st.session_state.memory.append(memory)

# ---- ANSWER ----
def generate_answer(state):
    memory_context = "\n".join(st.session_state.memory[-3:])  # last 3 memories

    if state["decision"] == "calculator":
        return {"final_answer": f"🧮 Result: {state['tool_output']}"}

    if state["decision"] == "web":
        prompt = f"""
        Use web results + memory:

        Memory:
        {memory_context}

        Web:
        {state['tool_output']}

        Question: {state['query']}
        """
        response = llm.invoke(prompt)
        return {"final_answer": f"🌐 {response.content}"}

    # normal answer with memory
    prompt = f"""
    Use memory if relevant:

    Memory:
    {memory_context}

    Question: {state['query']}
    """

    response = llm.invoke(prompt)
    return {"final_answer": response.content}

# ---- ROUTER ----
def route(state):
    return state["decision"]

# ---- GRAPH ----
builder = StateGraph(AgentState)

builder.add_node("decide", decide_action)
builder.add_node("calculator", calculator_tool)
builder.add_node("web", web_search_tool)
builder.add_node("answer", generate_answer)

builder.add_edge(START, "decide")

builder.add_conditional_edges(
    "decide",
    route,
    {
        "calculator": "calculator",
        "web": "web",
        "answer": "answer"
    }
)

builder.add_edge("calculator", "answer")
builder.add_edge("web", "answer")
builder.add_edge("answer", END)

graph = builder.compile()

# ---- UI ----
st.set_page_config(page_title="BrainSwitch AI", page_icon="🧠", layout="wide")

st.title("🧠 BrainSwitch")
st.caption(" Web + Tools + Remembers you as well 🧠  ")

# ---- INPUT ----
query = st.chat_input("Ask anything...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("🧠 Thinking with memory..."):
        result = graph.invoke({
            "query": query,
            "decision": "",
            "tool_output": "",
            "final_answer": ""
        })

    # update memory
    update_memory(query, result["final_answer"])

    st.session_state.messages.append({
        "role": "ai",
        "content": result["final_answer"],
        "decision": result["decision"]
    })

# ---- CHAT ----
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---- SIDEBAR ----
with st.sidebar:
    st.header("🧠 Brain Control")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

    if st.button("🧹 Clear Memory"):
        st.session_state.memory = []

    st.markdown("### 📌 Stored Memory")
    for mem in st.session_state.memory[-5:]:
        st.write("•", mem)

    st.markdown("---")
    st.success("Memory Active 🧠")
