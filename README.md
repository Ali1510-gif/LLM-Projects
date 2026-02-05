# 🐍 PyMentor v1  
### AI-Powered Python Coding Assistant

PyMentor v1 is a Streamlit-based AI chatbot built to help users with **Python programming questions only**.  
It uses OpenAI’s streaming responses to provide real-time answers in a chat-style interface.

This is **Version 1**, focused on core architecture, learning, and stability.

---

## 🚀 Features

- 🧠 Python-only AI mentor (non-Python queries are politely declined)
- ⚡ Real-time streaming responses (token-by-token)
- 💬 Chat-based UI using Streamlit
- 💾 Persistent chat history using JSON storage
- 🔐 Secure API key handling via environment variables
- 🧩 Modular and readable code structure

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Framework:** Streamlit  
- **AI API:** OpenAI Responses API  
- **Env Management:** python-dotenv  
- **Storage:** JSON (local)

---

## 📁 Project Structure

pymentor-v1/
├── app.py
├── chat_history.json
├── .env
├── requirements.txt
└── README.md


---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/pymentor-v1.git
cd pymentor-v1
2️⃣ Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Configure environment variables
Create a .env file:

OPENAI_API_KEY=your_openai_api_key_here
▶️ Run the Application
streamlit run app.py
Open the browser and start chatting with PyMentor.

🧠 How It Works
User submits a Python-related query

Messages are stored in Streamlit session state

OpenAI API is called with full chat context

Response is streamed live to the UI

Chat history is saved locally for persistence

⚠️ Limitations (v1)
Single-user support

JSON-based storage (not scalable)

No authentication

Basic error handling

No database integration

These are intentional trade-offs for the first version.

🔮 Roadmap (v2)
Multi-user support

Improved validation & error handling

Code snippets & syntax highlighting

Optional Python code execution

🎯 Learning Outcomes
AI chatbot architecture

Streaming API handling

Prompt engineering

State management in Streamlit

Secure API usage

👤 Author
Rayees Ali
Aspiring Software Engineer | Python & Java

⭐ If you find this project helpful, consider giving it a star!



