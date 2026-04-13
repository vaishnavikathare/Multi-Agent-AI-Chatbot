from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")   # make sure .env has key
)

# MAIN FUNCTION (IMPORTANT)
def run_ai(question):
    response = llm.invoke([
        HumanMessage(content=question)
    ])
    return response.content