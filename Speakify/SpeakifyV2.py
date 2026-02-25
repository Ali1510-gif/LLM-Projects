import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import base64
import time

# ======================================================
# 🔐 Setup
# ======================================================
load_dotenv()
client = OpenAI()

CHAT_DIR = "voice_chats"
os.makedirs(CHAT_DIR, exist_ok=True)

st.set_page_config(
    page_title="Speakify",
    page_icon="🎙️",
    layout="wide"
)

# ======================================================
# 🎨 ULTRA PREMIUM ANIMATED UI
# ======================================================
st.markdown("""
<style>

/* Animated Background */
body {
    background: linear-gradient(-45deg, #0f172a, #111827, #1e293b, #0f172a);
    background-size: 400% 400%;
    animation: gradientMove 20s ease infinite;
    color: #e5e7eb;
    font-family: 'Segoe UI', sans-serif;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Glass Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Logo Glow */
.logo-text {
    font-size: 60px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 8px;
    color: #f9fafb;
    animation: glow 3s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 6px rgba(59,130,246,0.5); }
    to { text-shadow: 0 0 18px rgba(59,130,246,0.9); }
}

/* Feature Pills */
.features {
    text-align: center;
    margin-bottom: 30px;
}

.feature-pill {
    display: inline-block;
    background: rgba(255,255,255,0.06);
    padding: 8px 14px;
    border-radius: 20px;
    margin: 6px;
    font-size: 13px;
    color: #cbd5e1;
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.3s ease;
}

.feature-pill:hover {
    background: rgba(59,130,246,0.2);
    transform: translateY(-3px);
}

/* Chat Container */
.chat-container {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Chat Bubbles */
.user-bubble {
    background: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 5px 18px;
    margin-bottom: 12px;
    max-width: 70%;
    margin-left: auto;
    animation: bubbleIn 0.4s ease;
}

.ai-bubble {
    background: rgba(255,255,255,0.08);
    color: #e2e8f0;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 5px;
    margin-bottom: 15px;
    max-width: 70%;
    animation: bubbleIn 0.4s ease;
}

@keyframes bubbleIn {
    from { opacity: 0; transform: scale(0.97); }
    to { opacity: 1; transform: scale(1); }
}

/* Typing Indicator */
.typing {
    display: inline-block;
    padding: 10px 14px;
    background: rgba(255,255,255,0.08);
    border-radius: 18px;
    font-size: 14px;
}

.typing span {
    display: inline-block;
    width: 6px;
    height: 6px;
    margin: 0 2px;
    background: #38bdf8;
    border-radius: 50%;
    animation: bounce 1.2s infinite;
}

.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}

/* Mic Pulse */
.pulse-mic {
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(59,130,246,0.7); }
    70% { box-shadow: 0 0 0 15px rgba(59,130,246,0); }
    100% { box-shadow: 0 0 0 0 rgba(59,130,246,0); }
}

/* Download link */
.download-link {
    color: #38bdf8;
    font-size: 13px;
    text-decoration: none;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# 📁 Chat Storage Functions
# ======================================================

def save_chat(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_chat(path):
    with open(path, "r") as f:
        return json.load(f)

def new_chat():
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(CHAT_DIR, f"{chat_id}.json")
    data = {
        "title": "New Voice Chat",
        "messages": [
            {"role": "system", "content": "You are Speakify, a professional AI voice assistant."}
        ]
    }
    save_chat(file_path, data)
    return chat_id

def list_chats():
    return sorted(os.listdir(CHAT_DIR), reverse=True)

def generate_chat_title(user_message):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "Generate short 4-word title."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.output_text.strip()

def prepare_messages_for_api(messages):
    return [{"role": m["role"], "content": m["content"]} for m in messages]

def stream_chat(messages, placeholder, temperature, model):
    clean = prepare_messages_for_api(messages)
    stream = client.responses.create(
        model=model,
        input=clean,
        temperature=temperature,
        stream=True
    )
    full = ""
    for event in stream:
        if event.type == "response.output_text.delta":
            full += event.delta
            placeholder.markdown(full)
    return full

# ======================================================
# Session Handling
# ======================================================

if "current_chat" not in st.session_state:
    st.session_state.current_chat = new_chat()

chat_files = list_chats()
chat_titles = {f: load_chat(os.path.join(CHAT_DIR, f))["title"] for f in chat_files}

with st.sidebar:
    st.header("⚙️ Settings")
    selected_chat = st.selectbox(
        "Select Chat",
        chat_files,
        index=chat_files.index(f"{st.session_state.current_chat}.json"),
        format_func=lambda x: chat_titles[x]
    )
    if selected_chat.replace(".json", "") != st.session_state.current_chat:
        st.session_state.current_chat = selected_chat.replace(".json", "")
        st.rerun()

    if st.button("➕ New Chat"):
        st.session_state.current_chat = new_chat()
        st.rerun()

    if st.button("🗑 Delete Chat"):
        os.remove(os.path.join(CHAT_DIR, f"{st.session_state.current_chat}.json"))
        st.session_state.current_chat = new_chat()
        st.rerun()

    st.markdown("---")

    voice_option = st.selectbox("🎙 Voice", ["marin", "alloy", "verse"])
    duration = st.slider("⏱ Duration", 3, 15, 8)
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-5.1"])
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)

# ======================================================
# Load Chat
# ======================================================

chat_path = os.path.join(CHAT_DIR, f"{st.session_state.current_chat}.json")
chat_data = load_chat(chat_path)
messages = chat_data["messages"]

# ======================================================
# Logo + Features
# ======================================================

st.markdown('<div class="logo-text">Speak🎙️fy</div>', unsafe_allow_html=True)

st.markdown("""
<div class="features">
<span class="feature-pill">🎙 Voice Recording</span>
<span class="feature-pill">🔄 Streaming AI</span>
<span class="feature-pill">🧠 Smart Titles</span>
<span class="feature-pill">💬 Multi-Chat</span>
<span class="feature-pill">🎛 Model Control</span>
<span class="feature-pill">🔊 Auto Voice Reply</span>
</div>
""", unsafe_allow_html=True)

# ======================================================
# Record with Pulse Animation
# ======================================================

if st.button("🎙 Start Recording", key="record_btn"):
    st.markdown('<div class="pulse-mic"></div>', unsafe_allow_html=True)

    with st.spinner("🎤 Recording..."):
        os.makedirs("audio", exist_ok=True)
        filename = "audio/input.wav"
        fs = 44100
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        write(filename, fs, recording)

    with st.spinner("🧠 Transcribing..."):
        with open(filename, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model="gpt-4o-transcribe"
            )
        user_text = transcript.text
        messages.append({"role": "user", "content": user_text})

        if chat_data["title"] == "New Voice Chat":
            chat_data["title"] = generate_chat_title(user_text)

    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="typing">
    Speakify is typing
    <span></span><span></span><span></span>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(1)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        ai_reply = stream_chat(messages, placeholder, temperature, model)

    typing_placeholder.empty()

    messages.append({"role": "assistant", "content": ai_reply})
    save_chat(chat_path, chat_data)

    with st.spinner("🔊 Generating Voice..."):
        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice_option,
            input=ai_reply
        )
        encoded = base64.b64encode(speech.read()).decode()
        messages[-1]["audio"] = encoded
        save_chat(chat_path, chat_data)

    st.rerun()

# ======================================================
# Display Chat with Auto Scroll
# ======================================================

st.markdown('<div class="chat-container" id="chat-box">', unsafe_allow_html=True)
st.markdown("### 💬 Conversation")

display_messages = [m for m in messages if m["role"] != "system"][::-1]

for msg in display_messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        if "audio" in msg:
            st.audio(base64.b64decode(msg["audio"]), format="audio/mp3", autoplay=True)
            st.markdown(
                f'<a class="download-link" href="data:audio/mp3;base64,{msg["audio"]}" download="reply.mp3">⬇ Download Audio</a>',
                unsafe_allow_html=True
            )

st.markdown('</div>', unsafe_allow_html=True)

# Smooth Auto Scroll
st.markdown("""
<script>
var chatBox = window.parent.document.querySelector('#chat-box');
if(chatBox){
    chatBox.scrollIntoView({behavior: "smooth", block: "start"});
}
</script>
""", unsafe_allow_html=True)
