# Import Streamlit library for building the web app UI
import streamlit as st
# Import OpenAI client for API calls
from openai import OpenAI 
# Import load_dotenv to read environment variables from .env file
from dotenv import load_dotenv
# Import json library to work with JSON files
import json 
# Import os library for file system operations
import os
# Import time library for adding delays
import time 
# Import datetime to generate timestamps for chat IDs
from datetime import datetime


# Define directory path to store chat history files
CHAT_DIR="chats"
# Create the 'chats' directory if it doesn't exist
os.makedirs(CHAT_DIR, exist_ok=True)








# Function to initialize and return OpenAI client
def get_open_ai_client():
    # Load environment variables from .env file (contains API keys)
    load_dotenv()
    # Return initialized OpenAI client instance
    return OpenAI()

# Create OpenAI client instance for making API calls
client=get_open_ai_client()


# Function to create a new chat session
def new_chat():
    # Generate unique chat ID using current timestamp (YYYYMMDD_HHMMSS format)
    chat_id=datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create file path for storing the chat messages
    file_path=os.path.join(CHAT_DIR, f"{chat_id}.json")
    
    # Initialize messages list with system prompt that defines ChatBot behavior
    messages=[{"role": "system", "content": "You are PyMentor, an AI assistant that helps users with Python programming questions. Provide clear and concise answers to the best of your ability."
                 "Answers only Python programming related questions."}]
    # Save the initial messages to the chat file
    save_chat(file_path,messages)
    # Return the unique chat ID
    return chat_id
    
    






# Function to save chat messages to a JSON file
def save_chat(path,messages):
    # Open file in write mode
    with open(path, "w") as f:
        # Serialize messages list to JSON and save with indentation
        json.dump(messages, f,indent=4)

# Function to load chat messages from a JSON file
def load_chat(path):
    # Open file in read mode
    with open(path, "r") as f:
        # Read and deserialize JSON data from file
        return json.load(f)

# Function to get list of all chat files in the chats directory
def list_chats():
   # Return sorted list of chat files in reverse order (newest first)
   return sorted(os.listdir(CHAT_DIR), reverse=True)





        



# Function to stream chat responses from AI model with real-time display
def stream_chat_with_ai(messages,placeholder,temperature,model ):
    # Create API request with streaming enabled
    stream=client.responses.create(
        # Specify which model to use
        model=model,
        # Pass conversation messages to the model
        input=messages,
        # Enable streaming to get real-time token responses
        stream=True,
        # Set temperature for response creativity (0.0=deterministic, 2.0=random)
        temperature=temperature,
        
        
        
        
        
        
        ) 
    
    # Initialize empty string to accumulate full response
    full_response=""
    
    # Iterate through each token received from the stream
    for event in stream:
        # Check if event is a text delta (partial response)
        if event.type=="response.output_text.delta":
            # Extract the token from the event
            token=event.delta
            # Append token to full response
            full_response+=token
            # Update placeholder with the streaming response in real-time
            placeholder.markdown(full_response)
    
    # Return the complete AI response
    return full_response
            
            
        
    
    
    
    

# Configure Streamlit page settings (title and layout)
st.set_page_config(page_title="PyMentor", layout="centered")

# Display main title with emoji
st.title(" 🐍 PyMentor - Your Python Coding ChatBot")

# Display welcome message
st.write(" ✨Welcome to PyMentor ! Your AI-powered Python coding assistant. Ask me anything about Python programming, and I'll do my best to help you out!")

# Display caption with features
st.caption("💡Streaming |💫 Resume Chat | 🎮 Controls Enabled |  Multiple Chats ")

# Add header in sidebar for chat settings
st.sidebar.header("🔑 Chat Settings") 

# Check if current_chat is not in session state (first run)
if "current_chat" not in st.session_state:
    # Initialize new chat session
    st.session_state.current_chat = new_chat()

# Get list of all saved chat files
chat_files=list_chats()
# Create dropdown to select previous chats from sidebar
selected_chat=st.sidebar.selectbox("Select Chat History", chat_files, index=chat_files.index(f"{st.session_state.current_chat}.json") )

# Check if selected chat is different from current chat
if selected_chat.replace(".json","") != st.session_state.current_chat:
    # Update current chat to the selected chat
    st.session_state.current_chat=selected_chat.replace(".json","")
    # Rerun the app to load the selected chat
    st.rerun()
    
# Create button to start a new chat session
if st.sidebar.button("➕ New Chat"):
    # Create new chat session
    st.session_state.current_chat=new_chat()
    # Rerun the app
    st.rerun()

# Create dropdown in sidebar to select AI model
model=st.sidebar.selectbox("Choose Model" ,["gpt-5.1","gpt-4.1-mini"])

# Create slider in sidebar to control temperature (creativity level)
temperature=st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)

# Construct the path to the current chat file
chat_path=os.path.join(CHAT_DIR, f"{st.session_state.current_chat}.json")
# Load all messages from the current chat file
messages=load_chat(chat_path)

# Count total messages excluding system messages
message_count=len([m for m in messages if m["role"]!="system"] )

# Display message count metric in sidebar
st.sidebar.metric("📧 Messages",message_count)

# Loop through all messages in the current chat
for msg in messages:
    # Check if message is not a system message
    if msg["role"] != "system":
        # Display the message in chat format with the role (user/assistant) as header
        st.chat_message(msg["role"], ).markdown(msg["content"])
    




    
# Create a form for user input that clears on submit
with st.form("chat_form", clear_on_submit=True):
    # Create text area for user input with placeholder text
    user_input = st.text_area("Ask me anything about Python:", height=100 ,placeholder="e.g., How do I create a function in Python?")

    # Create submit button labeled 'Ask PyMentor'
    submit_button = st.form_submit_button("Ask PyMentor")

    # Check if submit button is clicked and input is not empty
    if submit_button and user_input.strip() != "":
        # Display user message in chat interface
        st.chat_message("user", ).markdown(f"**You:** {user_input}")
        # Add user message to messages list
        messages.append({"role": "user", "content": user_input})
        
        # Create chat message container for assistant
        with st.chat_message("assistant"):
            # Create empty placeholder for typing indicator
            typing_placeholder = st.empty()
            # Display typing indicator
            typing_placeholder.markdown("⌛PyMentor is typing...")
            # Add small delay for better user experience
            time.sleep(0.5)  # Simulate typing delay
            # Create empty placeholder for actual response
            placeholder = st.empty()
            # Call AI function to get streaming response
            ai_reply=stream_chat_with_ai(messages,placeholder,temperature=temperature,model=model)
            # Clear the typing indicator
            typing_placeholder.write("")  # Clear the typing indicator
            
        # Add AI response to messages list
        messages.append({"role": "assistant", "content": ai_reply})     
        # Save updated messages to chat file
        save_chat(chat_path,messages)
        # Rerun the app to refresh display
        st.rerun()
        
# Create button in sidebar to clear current chat history
if st.sidebar.button("🧹 Clear Chat History"):
       # Delete the current chat file
       os.remove(chat_path)
       # Create a new chat session
       st.session_state.current_chat=new_chat()
       # Rerun the app to refresh with new chat
       st.rerun()
         
        

        
    

        
        
        
    
        
    





