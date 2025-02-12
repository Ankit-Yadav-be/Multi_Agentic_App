import subprocess
import shutil
import os

def create_python_virtualenv(project_name):
    # Build the project path
    project_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", project_name)

    # Check if the directory exists and remove it if necessary
    if os.path.exists(project_path):
        shutil.rmtree(project_path)

    try:
        # Create the project directory
        os.makedirs(project_path, exist_ok=True)

        # Create a conda virtual environment
        subprocess.run([f"conda", "create", "--prefix", f"{project_path}\\venv", "python=3.10", "-y"], check=True)

        # Activate the environment
        activate_env = f"conda activate {project_path}\\venv"

        # Create a requirements.txt file (list the necessary dependencies)
        requirements = [
            "requests",
            "streamlit",
            "speechrecognition",
            "langgraph"
        ]

        with open(os.path.join(project_path, "requirements.txt"), "w", encoding="utf-8") as req_file:
            for req in requirements:
                req_file.write(f"{req}\n")

        # Install dependencies from the requirements.txt
        subprocess.run(f"{activate_env} && pip install -r {project_path}\\requirements.txt", shell=True, check=True)

        # ✅ Create chat.py file with the provided code
        chat_code = """
import requests
import streamlit as st
import speech_recognition as sr
from langgraph.graph import StateGraph
from typing import TypedDict

# ✅ Replace this with your actual Gemini API Key
gemini_api_key = "AIzaSyANKZXIvvJGTe1ZRK4CAZ_ilfsRkjOxnv4"

# ✅ Define chatbot state schema
class ChatState(TypedDict):
    message: str

# ✅ Function to get response from Gemini AI
def get_gemini_response(state: ChatState) -> ChatState:
    prompt = state["message"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}  

    response = requests.post(url, json=data, headers=headers)
    
    try:
        response_json = response.json()
        
        if "candidates" in response_json:
            return {"message": response_json["candidates"][0]["content"]["parts"][0]["text"]}
        elif "error" in response_json:
            return {"message": f"API Error: {response_json['error']['message']}"}
        else:
            return {"message": "Unexpected API Response!"}
    except Exception as e:
        return {"message": f"Exception Occurred: {str(e)}"}

# ✅ Create LangGraph workflow
graph = StateGraph(ChatState)  
graph.add_node("user_input", get_gemini_response)
graph.set_entry_point("user_input")
workflow = graph.compile()

# ✅ Streamlit UI
st.set_page_config(page_title="AI voice chatbot", page_icon="🎙️", layout="centered")

st.title("🎙️ Ankit Yadav Personal AI voice chatbot")
st.write("Speak to ask your questions! (Powered by Google Gemini llm model & LangGraph)")

# ✅ Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display chat history
for chat in st.session_state.messages:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# ✅ Speech recognition function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio. Please try again."
        except sr.RequestError:
            return "Could not request results. Check your internet connection."

# ✅ Button to start voice input
if st.button("🎙️ Speak Now"):
    user_input = recognize_speech()
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # ✅ Get AI response
    response = workflow.invoke({"message": user_input})
    bot_reply = response["message"]

    # ✅ Show bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
"""
        
        # Save the chat.py file
        with open(os.path.join(project_path, "chat.py"), "w", encoding="utf-8") as chat_file:
            chat_file.write(chat_code)

        print("✅ Virtual environment created, dependencies installed, and chat.py created successfully!")
        return project_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating virtual environment or installing dependencies: {e}")
        return None
