import streamlit as st
from school_ai import graph   # import your main AI pipeline

st.set_page_config(page_title="AI Agent", layout="centered")

st.title("🤖 Multi-Agent AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Ask something:")

if st.button("Send") and user_input:

    result = graph.invoke({"question": user_input})

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("AI", result["answer"]))

for sender, message in st.session_state.messages:
    st.write(f"**{sender}:** {message}")