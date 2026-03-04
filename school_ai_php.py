from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from dotenv import load_dotenv
import requests
import os

# -------------------------
# 🔑 Groq API
# -------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
     api_key=os.getenv("YOUR API KEY")
)

# -------------------------
# 📊 Google Sheets Setup
# -------------------------
scope = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client_sheet = gspread.authorize(creds)

sheet = client_sheet.open_by_key(
    "1GKu47q_6g7DTWVxQXXyJ7hfBVtjCkizmlJooUN7X4tc"
).sheet1


# -------------------------
# State Schema
# -------------------------
class StudentState(TypedDict, total=False):
    question: str
    answer: str


# -------------------------
# Node 1: Get Question
# -------------------------
def get_question(state):
    question = input("👋 Ask English Buddy: ")
    return {"question": question}


# -------------------------
# Node 2: AI Teaching Logic
# -------------------------
def ask_ai(state):
    system_prompt = """
You are English Buddy 📚✨
Target: Grades 1-5 students.

Rules:
• Add emojis 🎉
• Use bullet points •
• Add INDEX at start
• Max 60 characters per line
• Add short story example
• Keep language simple
"""

    response = llm.invoke([
        HumanMessage(
            content=system_prompt +
            "\n\nStudent Question: " +
            state["question"]
        )
    ])

    return {"answer": response.content}


# -------------------------
# Node 3: Show + Save
# -------------------------
def show_answer(state):
    print("\n📚 English Buddy Says:\n")
    print(state["answer"])


    # Send data to PHP backend
    url = "http://localhost/save_data.php"

    payload = {
        "question": state["question"],
        "answer": state["answer"]
    }

    try:
        response = requests.post(url, json=payload)
        print("\n✅ Saved to PHP Database!")
    except Exception as e:
        print("Error saving to PHP:", e)
   
    return {}


# -------------------------
# Build Graph
# -------------------------
builder = StateGraph(StudentState)

builder.add_node("input", get_question)
builder.add_node("ai", ask_ai)
builder.add_node("output", show_answer)

builder.set_entry_point("input")

builder.add_edge("input", "ai")
builder.add_edge("ai", "output")
builder.add_edge("output", END)

graph = builder.compile()


# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    graph.invoke({})