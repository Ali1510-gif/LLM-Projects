<img width="1869" height="692" alt="image" src="https://github.com/user-attachments/assets/ccd103ae-75d4-4df6-aade-4c675fb07987" />




# 🎙 Speakify v2 — AI Voice Assistant

> A premium multi-chat AI Voice Assistant built with Streamlit + OpenAI APIs  
> Real-time voice recording • Streaming AI • Auto TTS • Smart Chat Titles • Persistent Storage

---

## 🚀 Features

- 🎙 Real-Time Voice Recording  
- 🧠 Streaming AI Responses  
- 🔊 Automatic Text-to-Speech Replies  
- 💬 Multi-Chat Management System  
- 🏷 Smart AI-Generated Chat Titles  
- 💾 Persistent JSON Chat Storage  
- ⬇ Download AI Voice Replies  
- 🎛 Model & Temperature Control  
- 🎨 Premium Animated Glass UI  

---

## 🧠 Tech Stack

- **Frontend:** Streamlit  
- **AI Models:** GPT-4o-mini / GPT-5.1  
- **Speech-to-Text:** gpt-4o-transcribe  
- **Text-to-Speech:** gpt-4o-mini-tts  
- **Audio Recording:** sounddevice  
- **Storage:** JSON File System  
- **Styling:** Custom CSS + Glassmorphism UI  

---

## 📂 Project Structure

```
Speakify/
│
├── voice_chats/        # Stored conversations (JSON)
├── audio/              # Temporary audio recordings
├── app.py              # Main Application
├── .env                # OpenAI API Key
└── README.md
```

---

## 🛠 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Speakify.git
cd Speakify
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install streamlit openai python-dotenv sounddevice scipy
```

Or create a `requirements.txt` and run:

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add OpenAI API Key

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_api_key_here
```

---

### 5️⃣ Run Application

```bash
streamlit run app.py
```

---

## ⚙ Sidebar Controls

- 🎙 Select Voice  
- ⏱ Recording Duration  
- 🧠 Select Model  
- 🌡 Temperature Adjustment  
- ➕ Create New Chat  
- 🗑 Delete Chat  

---

## 💡 How It Works

1. 🎤 User records voice  
2. 📜 Audio is transcribed using OpenAI  
3. 🧠 AI generates streamed response  
4. 🔊 Response converted into speech  
5. 💾 Conversation saved locally as JSON  
6. 🎧 Voice auto-plays with download option  

---

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| OPENAI_API_KEY | Your OpenAI Secret Key |

---

## 📌 What This Project Demonstrates

- Real-time AI streaming  
- Voice-to-text & text-to-speech pipeline  
- Stateful multi-chat system  
- Local persistent storage architecture  
- Advanced UI/UX design with animations  
- Practical OpenAI API integration  

---

## 🔮 Future Improvements

- 🌍 Multi-language response selection  
- 🧠 Long-term memory compression  
- ☁ Cloud database integration  
- 🔐 User authentication  
- 🚀 Deployment on Streamlit Cloud / Render  

---

## 👨‍💻 Author

**Rayees Ali**  
B.Tech CSE | AI Enthusiast | Full Stack Developer  

- Exploring AI + Web + Voice Systems  
- Open to Internship & Entry-Level Opportunities  

---

## ⭐ Support

If you like this project:

- Give it a ⭐ on GitHub  
- Fork and build your own AI Assistant  
- Share it with others  

---
