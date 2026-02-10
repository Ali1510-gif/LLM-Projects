
# 🐍 PyMentor v3.0.0  
### Architecture & Multi-Chat Upgrade 🚀

PyMentor is a **Python-only AI coding assistant** built using **Streamlit** and **OpenAI**.  
It helps users learn and debug Python through an interactive, chat-based interface.

Version **v3.0.0** introduces a major architectural upgrade, transforming PyMentor from a UX-focused demo into a **scalable, product-grade AI system**.

---

## ✨ Features

### 🆕 Added
- Multi-chat support with independent conversations
- Timestamp-based chat sessions
- Sidebar chat history selector
- New chat creation functionality
- Per-chat clear history option
- Organized `chats/` directory (one JSON file per chat)

### 🛠 Improved
- File-based chat architecture for scalability
- Robust Streamlit session state management
- Clear separation of UI, state, and storage logic
- Smooth chat switching with better rerun handling
- Cleaner and more maintainable code structure

---

## ⚠️ Known Limitations
- Single-user support only
- Local file-based storage (no database)
- No authentication system
- Chat titles are timestamp-based (not semantic yet)

---

## 🎯 Purpose of This Release
PyMentor v3 focuses on **architecture, scalability, and system design**.

This version moves beyond feature additions and lays a strong foundation for a **polished final release**, enabling multiple chat sessions and cleaner data management.

---

## 🔮 Roadmap

### 🚀 v4.0.0 — Final Version
- Chat titles shown as file names (ChatGPT-style)
- Intelligent or user-editable chat naming
- Refined and finalized UX/UI
- Optimized and locked architecture
- Stability-focused, no major refactors

---

## 🛠 Tech Stack
- Python
- Streamlit
- OpenAI Responses API
- JSON-based local storage
- python-dotenv

---

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/pymentor.git
cd pymentor
pip install -r requirements.txt
