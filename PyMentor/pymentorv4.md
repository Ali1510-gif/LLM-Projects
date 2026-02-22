# 🐍 PyMentor v4.0.0  
### Final Stable Release – Product Polish Upgrade 🚀  

PyMentor is a **Python-only AI coding assistant** built using **Streamlit** and **OpenAI**.  
It helps users learn, debug, and understand Python concepts through an interactive chat-based interface.

Version **v4.0.0** represents the **final stable release**, focusing on product refinement, conversation identity, and a more professional AI assistant experience.

---

## ✨ Features  

### 🆕 Added  
- Automatic chat title generation (ChatGPT-style)  
- Structured chat metadata (`title + messages`)  
- Semantic conversation naming instead of timestamps  
- Improved sidebar display with readable chat titles  
- Intelligent first-message-based title creation  
- Refined delete chat behavior  

### 🛠 Improved  
- Cleaner and modular chat lifecycle structure  
- Improved system prompt for stricter Python-only behavior  
- Better separation of metadata and message handling  
- More maintainable storage architecture  
- Enhanced overall UX polish and clarity  

---

## ⚠️ Known Limitations  
- Single-user support only  
- Local file-based storage (no database)  
- No authentication system  
- No cloud deployment configuration by default  
- No chat search or tagging system  

---

## 🎯 Purpose of This Release  

PyMentor v4 focuses on **product polish, conversation identity, and UX refinement**.

This version completes the architectural journey started in v3 by:

- Making conversations meaningful (title-based)  
- Structuring chat data for future expansion  
- Delivering a more professional, SaaS-like experience  

PyMentor now behaves like a **real AI product**, not just a demo project.

---

## 🔮 Future Enhancements (Optional Roadmap)

Even though v4 is the final stable release, future improvements may include:

- 🔐 User authentication  
- ☁️ Cloud database integration  
- 🔎 Chat search functionality  
- 🏷 Chat tagging system  
- 🌍 Multi-user support  
- 🚀 Production deployment setup  
- 📊 Usage analytics  

---

## 🛠 Tech Stack  

- Python  
- Streamlit  
- OpenAI Responses API  
- JSON-based structured storage  
- python-dotenv  

---

## 🚀 Getting Started  

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/pymentor.git
cd pymentor
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Create `.env` file

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_api_key_here
```

### 4️⃣ Run the application

```bash
streamlit run app.py
```

---

## 📌 Version Evolution

- **v1** → Core chatbot foundation  
- **v2** → UX & control enhancements  
- **v3** → Multi-chat & scalable architecture  
- **v4** → Final product polish & semantic conversations  

---

## 📄 License

This project is built for learning and portfolio purposes.  
Feel free to fork, improve, and build upon it.

---

## 🙌 Author

**Rayees Ali**  
Building → Learning → Improving → Repeating 🚀
