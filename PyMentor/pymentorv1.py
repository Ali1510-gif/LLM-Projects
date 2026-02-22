import streamlit as st
from openai import OpenAI 
from dotenv import load_dotenv
import json 
import os




CHAT_FILE="chat_history.json"

def get_open_ai_client():
    load_dotenv()
    return OpenAI()

client=get_open_ai_client()

def save_chat_history(messages):
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f,indent=4)

def load_chat_history():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    else:
        return [{"role": "system", "content": "You are PyMentor, an AI assistant that helps users with Python programming questions. Provide clear and concise answers to the best of your ability."
                 "Answers only Python programming related questions." 
                 " Politely decline to answer questions that are not related to Python programming."}]


        



def stream_chat_with_ai(messages,placeholder):
    stream=client.responses.create(model="gpt-5.1",input=messages,stream=True,) 
    
    full_response=""
    
    for event in stream:
        if event.type=="response.output_text.delta":
            token=event.delta
            full_response+=token
            placeholder.markdown(full_response)
    
    return full_response
            
            
        
    
    
    
    

st.set_page_config(page_title="PyMentor", layout="centered")


st.title(" 🐍 PyMentor - Your Python Coding ChatBot")


st.write(" ✨Welcome to PyMentor ! Your AI-powered Python coding assistant. Ask me anything about Python programming, and I'll do my best to help you out!")


if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

for msg in st.session_state.messages:
    
    if msg["role"] != "system":
        
     st.chat_message(msg["role"], ).markdown(msg["content"])
    




    
with st.form("chat_form", clear_on_submit=True):
    
    user_input = st.text_area("Ask me anything about Python:", height=100 ,placeholder="e.g., How do I create a function in Python?")

    submit_button = st.form_submit_button("Ask PyMentor")

if submit_button:
    
    if user_input.strip() == "":
        st.warning("Please enter a question before submitting.")
    
    else:
        
        st.chat_message("user", ).markdown(f"**You:** {user_input}")
        st.session_state.messages.append({"role": "user", "content": user_input})
        #Ai call()
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            ai_reply=stream_chat_with_ai(st.session_state.messages,placeholder)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})     
           
           
    save_chat_history(st.session_state.messages)
        
    st.rerun()
        
    
    

        
        
        
    
        
    





