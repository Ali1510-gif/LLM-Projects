import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

# -------------------- CONFIG --------------------
load_dotenv()
DB_DIR = "./db"

st.set_page_config(page_title="AI PDF Assistant", layout="wide", page_icon="📄")

# -------------------- MODERN CSS --------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Center container */
.main-container {
    max-width: 900px;
    margin: auto;
}

/* Header */
.header {
    text-align: center;
    margin-bottom: 20px;
}

.header h1 {
    font-size: 2.5rem;
    font-weight: 700;
}

/* Chat bubbles */
.user-msg {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: white;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 10px 0;
    text-align: right;
}

.bot-msg {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 12px 16px;
    border-radius: 15px;
    margin: 10px 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* Buttons */
.stButton button {
    border-radius: 10px;
    width: 100%;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 1px dashed #3b82f6;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOGIC (UNCHANGED) --------------------
@st.cache_resource
def create_vector_db(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    if not chunks:
        raise ValueError("No content found in PDF.")

    embeddings = OpenAIEmbeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    vectorstore.persist()
    return vectorstore


def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 3})


def get_prompt():
    return ChatPromptTemplate.from_template("""
    Answer the question based on the following context:

    {context}

    Question: {question}
    """)


def format_docs(docs):
    return "\n\n".join(f"- {doc.page_content}" for doc in docs)


# -------------------- SESSION --------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("⚙️ Controls")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        with st.spinner("Processing PDF..."):
            st.session_state.vectorstore = create_vector_db(temp_path)

        st.success("✅ PDF Ready")

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("🔄 Reset DB"):
        import shutil
        if os.path.exists(DB_DIR):
            shutil.rmtree(DB_DIR)
        st.session_state.vectorstore = None
        st.success("Database Reset")

# -------------------- MAIN UI --------------------
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.markdown("""
<div class='header'>
    <h1>📄 AI PDF Assistant</h1>
    <p>Chat with your document like ChatGPT</p>
</div>
""", unsafe_allow_html=True)

# Empty state
if not st.session_state.vectorstore:
    st.info("👈 Upload a PDF from sidebar to get started")

query = st.chat_input("Ask something about your PDF...")

# -------------------- RESPONSE --------------------
if query:
    if not st.session_state.vectorstore:
        st.warning("Upload PDF first")
    else:
        st.session_state.chat_history.append(("user", query))

        retriever = get_retriever(st.session_state.vectorstore)
        prompt = get_prompt()
        llm = ChatOpenAI(model="gpt-4o-mini")

        with st.spinner("Thinking..."):
            docs = retriever.invoke(query)

            if not docs:
                answer = "No relevant information found."
                sources = []
            else:
                context = format_docs(docs)
                final_prompt = prompt.format(context=context, question=query)
                response = llm.invoke(final_prompt)
                answer = response.content
                sources = docs

        st.session_state.chat_history.append(("bot", answer))
        st.session_state["sources"] = sources

# -------------------- CHAT DISPLAY --------------------
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"<div class='user-msg'>🧑 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>🤖 {msg}</div>", unsafe_allow_html=True)

# -------------------- SOURCES --------------------
if "sources" in st.session_state:
    with st.expander("🔍 Sources"):
        for i, doc in enumerate(st.session_state["sources"]):
            st.write(f"Chunk {i+1}")
            st.write(doc.page_content[:400])
            st.divider()

st.markdown("</div>", unsafe_allow_html=True)
