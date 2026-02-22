# ==============================
# 🐍 PyMentor - Python Tutor Chatbot
# Built with Streamlit + OpenAI Responses API
# Features:
# - Multiple Chats
# - Chat Titles Generation
# - Streaming AI Response
# - Temperature & Model Control
# - Persistent Chat Storage (JSON)
# ==============================

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import time
from datetime import datetime


# ==============================
# 📁 Chat Storage Setup
# ==============================

# Directory where all chat JSON files will be stored
CHAT_DIR = "chats"

# Create folder if it does not exist
os.makedirs(CHAT_DIR, exist_ok=True)


# ==============================
# 🔐 Initialize OpenAI Client
# ==============================

def get_open_ai_client():
    """
    Load environment variables and return OpenAI client.
    Make sure your API key is stored in .env file.
    """
    load_dotenv()
    return OpenAI()


# Create client instance
client = get_open_ai_client()


# ==============================
# 🆕 Create New Chat
# ==============================

def new_chat():
    """
    Creates a new chat file with:
    - Unique timestamp ID
    - Default system prompt
    """
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(CHAT_DIR, f"{chat_id}.json")

    # Initial chat structure
    data = {
        "title": "New Chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are PyMentor, a helpful Python Tutor. "
                    "Answer only Python related questions. "
                    "Politely refuse non-Python questions."
                )
            }
        ]
    }

    save_chat(file_path, data)
    return chat_id


# ==============================
# 💾 Save Chat to File
# ==============================

def save_chat(path, data):
    """
    Save chat data (title + messages) into JSON file.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# ==============================
# 🏷 Generate Chat Title
# ==============================

def generate_chat_title(user_message):
    """
    Generate a short title (max 5 words)
    based on the first user message.
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Generate a short title (max 5 words) "
                    "based on user message. "
                    "Do not use quotes."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.output_text.strip()


# ==============================
# 📂 Load Existing Chat
# ==============================

def load_chat(path):
    """
    Load chat JSON file.
    """
    with open(path, "r") as f:
        return json.load(f)


# ==============================
# 📋 List All Chats
# ==============================

def list_chats():
    """
    Return list of all chat files sorted by latest first.
    """
    return sorted(os.listdir(CHAT_DIR), reverse=True)


# ==============================
# 🔄 Stream AI Response
# ==============================

def stream_chat_with_ai(messages, placeholder, temperature, model):
    """
    Stream response token-by-token from OpenAI.
    Display live output in Streamlit.
    """
    stream = client.responses.create(
        model=model,
        input=messages,
        temperature=temperature,
        stream=True
    )

    full_response = ""

    for event in stream:
        # Check for streaming text token
        if event.type == "response.output_text.delta":
            token = event.delta
            full_response += token
            placeholder.markdown(full_response)

    return full_response


# ==============================
# 🎨 Streamlit Page Config
# ==============================

st.set_page_config(page_title="PyMentor", layout="centered")

st.title("🐍 PyMentor - Python Tutor ChatBot")
st.write("💡 Welcome To Your AI Powered Python Assistant")
st.caption("🧚‍♀️ Chat Titles | 💬 Streaming | 🔄 Resume Chat | 🎮 Controls | 🤹 Multiple Chats")


# ==============================
# ⚙️ Sidebar Settings
# ==============================

st.sidebar.header("⚙️ Chat Settings")

# Initialize session state for current chat
if "current_chat" not in st.session_state:
    st.session_state.current_chat = new_chat()

# Load all chats
chat_files = list_chats()

# Store titles for dropdown display
chat_titles = {}

for f in chat_files:
    data = load_chat(os.path.join(CHAT_DIR, f))
    chat_titles[f] = data["title"]

# Chat selection dropdown
selected_chat = st.sidebar.selectbox(
    "Select Chat",
    chat_files,
    index=chat_files.index(f"{st.session_state.current_chat}.json"),
    format_func=lambda f: chat_titles[f]
)

# If user switches chat
if selected_chat.replace(".json", "") != st.session_state.current_chat:
    st.session_state.current_chat = selected_chat.replace(".json", "")
    st.rerun()

# Create new chat button
if st.sidebar.button("➕ New Chat"):
    st.session_state.current_chat = new_chat()
    st.rerun()

# Model selection
model = st.sidebar.selectbox("Choose Model", ["gpt-5.1", "gpt-4.1-mini"])

# Temperature control
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1
)


# ==============================
# 📥 Load Current Chat
# ==============================

chat_path = os.path.join(CHAT_DIR, f"{st.session_state.current_chat}.json")
chat_data = load_chat(chat_path)
messages = chat_data["messages"]

# Count only user & assistant messages
message_count = len([m for m in messages if m["role"] != "system"])
st.sidebar.metric("💬 Messages", message_count)


# ==============================
# 💬 Display Chat Messages
# ==============================

for msg in messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).markdown(msg["content"])


# ==============================
# 📝 Chat Input Form
# ==============================

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Ask a Python Question",
        height=100,
        placeholder="For eg: Explain Python List with examples"
    )
    submit = st.form_submit_button("Ask PyMentor")


# ==============================
# 🤖 Handle User Submission
# ==============================

if submit and user_input.strip():

    # Show user message
    st.chat_message("user").markdown(user_input)
    messages.append({"role": "user", "content": user_input})

    # Generate title if first message
    if chat_data["title"] == "New Chat":
        chat_data["title"] = generate_chat_title(user_input)

    # Display assistant response
    with st.chat_message("assistant"):

        # Typing indicator
        typing = st.empty()
        typing.markdown("⌛ PyMentor Is Typing...")
        time.sleep(0.5)

        placeholder = st.empty()

        # Stream response
        ai_reply = stream_chat_with_ai(
            messages,
            placeholder,
            temperature=temperature,
            model=model
        )

        typing.write("")

    # Save assistant message
    messages.append({"role": "assistant", "content": ai_reply})
    save_chat(chat_path, chat_data)

    st.rerun()


# ==============================
# 🗑 Delete Chat
# ==============================

if st.sidebar.button("🗑️ Delete Chat"):
    os.remove(chat_path)
    st.session_state.current_chat = new_chat()
    st.rerun()
