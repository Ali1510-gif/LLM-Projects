
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
import base64

# ---------------------------
# Setup
# ---------------------------
load_dotenv()
client = OpenAI()

st.set_page_config(
    page_title="Speakify",
    page_icon="🎙️",
    layout="wide"
)

# ---------------------------
# Custom Colorful UI
# ---------------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.main {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

.title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    color: white;
}

.feature-badge {
    display: inline-block;
    padding: 8px 14px;
    margin: 5px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    color: white;
}

.badge1 { background-color: #ff6b6b; }
.badge2 { background-color: #4ecdc4; }
.badge3 { background-color: #f7b731; }
.badge4 { background-color: #20bf6b; }
.badge5 { background-color: #45aaf2; }

.chat-user {
    background: #E8F0FE;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}

.chat-ai {
    background: #F1F3F4;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
}

.stButton>button {
    background: linear-gradient(90deg, #ff6b6b, #f7b731);
    color: white;
    border-radius: 8px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Session Memory
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    voice_option = st.selectbox(
        "🎤 Select Voice",
        ["marin", "alloy", "verse"]
    )

    if st.button("🗑 Clear Conversation"):
        st.session_state.messages = []
        st.success("Conversation Cleared")

    st.markdown("---")
    st.write("Built with ❤️ using OpenAI")

# ---------------------------
# Header Section
# ---------------------------
st.markdown('<div class="title">🎙️ Speakify</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:10px;">
<span class="feature-badge badge1">🎧 Voice to Text</span>
<span class="feature-badge badge2">🧠 AI Context Memory</span>
<span class="feature-badge badge3">🔊 Text to Speech</span>
<span class="feature-badge badge4">⬇ Download Audio</span>
<span class="feature-badge badge5">⚡ Real-Time Processing</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------
# Upload Section
# ---------------------------
uploaded_file = st.file_uploader(
    "Upload Your Voice Message",
    type=["wav", "mp3", "m4a"]
)

if uploaded_file:

    with st.spinner("✨ Speakify is processing your voice..."):

        os.makedirs("temp", exist_ok=True)
        temp_path = f"temp/{uploaded_file.name}"

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        # 1️⃣ Transcription
        with open(temp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model="gpt-4o-transcribe"
            )

        user_text = transcript.text

        st.session_state.messages.append({
            "role": "user",
            "content": user_text
        })

        # 2️⃣ Context-aware AI Response
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": "You are Speakify, a professional AI voice assistant. Keep responses conversational and concise."}
            ] + st.session_state.messages
        )

        ai_reply = response.output_text

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

        # 3️⃣ Text to Speech
        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice_option,
            input=ai_reply
        )

        audio_bytes = speech.read()

        # Save audio
        os.makedirs("audio", exist_ok=True)
        filename = f"audio/{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"

        with open(filename, "wb") as f:
            f.write(audio_bytes)

        st.session_state.messages[-1]["audio"] = audio_bytes

# ---------------------------
# Chat Display
# ---------------------------
if st.session_state.messages:

    st.markdown("## 💬 Conversation")

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            st.markdown('<div class="chat-user">', unsafe_allow_html=True)
            st.markdown(f"**You:** {msg['content']}")
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown('<div class="chat-ai">', unsafe_allow_html=True)
            st.markdown(f"**Speakify:** {msg['content']}")
            
            if "audio" in msg:
                st.audio(msg["audio"], format="audio/mp3")

                b64 = base64.b64encode(msg["audio"]).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="speakify_reply.mp3">⬇ Download Audio</a>'
                st.markdown(href, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
