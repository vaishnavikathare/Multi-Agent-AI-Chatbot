from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from langgraph.graph import START
from dotenv import load_dotenv
import os

load_dotenv()

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
    agent: str
    answer: str


# -------------------------
# Node 1: Get Question
# -------------------------
def get_question(state):
    question = input("👋 Ask Agent AI: ")
    return {"question": question}


# -------------------------
# English Agent
# -------------------------
def ask_ai(state):
    system_prompt = """
You are English Buddy 📚✨
Target: Grades 1-5 students.
Use simple language and emojis.
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
# Router Agent
# -------------------------
def route_agent(state):
    router_prompt = """
Classify the user query into ONE category only:

English
Coding
DataScience
CyberSecurity
Career

Return only one word.
"""

    response = llm.invoke([
        HumanMessage(
            content=router_prompt +
            "\n\nUser Question: " +
            state["question"]
        )
    ])

    return {"agent": response.content.strip()}


# -------------------------
# Coding Agent
# -------------------------
def coding_agent(state):
    prompt = """
You are a Coding Expert 💻
Explain clearly.
Give example code.
"""

    response = llm.invoke([
        HumanMessage(content=prompt + "\n\nQuestion: " + state["question"])
    ])

    return {"answer": response.content}


# -------------------------
# Data Science Agent
# -------------------------
def data_science_agent(state):
    prompt = """
You are a Data Science Expert 📊
Explain AI, ML clearly with examples.
"""

    response = llm.invoke([
        HumanMessage(content=prompt + "\n\nQuestion: " + state["question"])
    ])

    return {"answer": response.content}


# -------------------------
# Cyber Security Agent
# -------------------------
def cybersecurity_agent(state):
    prompt = """
You are a Cyber Security Expert 🔐
Explain threats and prevention.
Use bullet points.
"""

    response = llm.invoke([
        HumanMessage(content=prompt + "\n\nQuestion: " + state["question"])
    ])

    return {"answer": response.content}


# -------------------------
# Career Agent
# -------------------------
def career_agent(state):
    prompt = """
You are a Career Guidance Expert 🎯
Suggest roadmap and skills.
Be practical.
"""

    response = llm.invoke([
        HumanMessage(content=prompt + "\n\nQuestion: " + state["question"])
    ])

    return {"answer": response.content}


# -------------------------
# Selector Agent
# -------------------------
def select_agent(state):

    if state["agent"] == "English":
        return ask_ai(state)

    elif state["agent"] == "Coding":
        return coding_agent(state)

    elif state["agent"] == "DataScience":
        return data_science_agent(state)

    elif state["agent"] == "CyberSecurity":
        return cybersecurity_agent(state)

    elif state["agent"] == "Career":
        return career_agent(state)

    else:
        return ask_ai(state)


# -------------------------
# Node 3: Show + Save
# -------------------------
def show_answer(state):
    print("\n🤖 AI Says:\n")
    print(state["answer"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([
        now,
        state["question"],
        state["answer"]
    ])

    print("\n✅ Saved to Google Sheet!")
    return {}


# -------------------------
# Build Graph
# -------------------------


builder = StateGraph(StudentState)

# Add nodes
builder.add_node("router", route_agent)
builder.add_node("selector", select_agent)
builder.add_node("output", show_answer)

# Set START properly
builder.add_edge(START, "router")

builder.add_edge("router", "selector")
builder.add_edge("selector", "output")
builder.add_edge("output", END)

graph = builder.compile()

# -------------------------
# Run App
# -------------------------
# if __name__ == "__main__":
#     graph.invoke({})