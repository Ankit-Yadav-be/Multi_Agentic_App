import os
import streamlit as st
import sqlite3
import datetime
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

# ✅ Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_KEY")

# ✅ Initialize LLM (Groq)
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="Gemma2-9b-It")

class State(TypedDict):
    message: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot(state: State):
    query = state['message'][-1].content if hasattr(state['message'][-1], "content") else state['message'][-1]
    final_response = llm.invoke(f"User Query: {query}\nAssistant Response:")
    return {"message": final_response}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# ✅ Database setup
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, task TEXT, due_date TEXT, reminder_time TEXT)''')
    conn.commit()
    conn.close()

init_db()

def add_task(task, due_date, reminder_time):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, due_date, reminder_time) VALUES (?, ?, ?)", (task, due_date, reminder_time))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

# ✅ Streamlit UI
st.title("🚀 AI Todo & Reminder System")
st.write("Add your tasks and get smart AI reminders!")

task = st.text_input("Task Name")
due_date = st.date_input("Due Date", datetime.date.today())
reminder_time = st.text_input("Reminder Time (HH:MM)")

if st.button("Add Task ✅"):
    add_task(task, str(due_date), reminder_time)
    st.success("Task Added Successfully!")

tasks = get_tasks()
st.write("## Your Tasks")
for t in tasks:
    st.write(f"🔹 {t[1]} - Due: {t[2]} - Reminder: {t[3]}")

# ✅ Reminder Checking
def check_reminders():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tasks = get_tasks()
    for t in tasks:
        task_time = f"{t[2]} {t[3]}"  # Combine due date and time
        if now == task_time:
            st.warning(f"🔔 Reminder: {t[1]} is due now!")

# ✅ Refresh every 30 seconds
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()

# ✅ Check Reminders
check_reminders()

# ✅ Chatbot Integration
st.write("## 🤖 AI Assistant")
st.write("Ask anything!")

user_input = st.text_input("You:", "")

if user_input:
    with st.spinner("🤖 Thinking..."):
        for event in graph.stream({'message': ["user", user_input]}):
            for value in event.values():
                st.write("🤖 Assistant:", value["message"].content)
