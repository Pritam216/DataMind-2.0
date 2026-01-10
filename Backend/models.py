from langchain_cohere import ChatCohere
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import logging

load_dotenv()

llm_google_1 = ChatGoogleGenerativeAI(
    model = "gemini-2.5-pro",
    temperature = 0.3,
    api_key = os.environ["GEMINI_API_KEY"],
)

llm_google_2 = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-lite",
    temperature = 0.3,
    api_key = os.environ["GEMINI_API_KEY"],
)

llm_google_3 = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature = 0.3,
    api_key = os.environ["GEMINI_API_KEY"],
)

llm_cohere = ChatCohere(
    model="command-a-03-2025",
    temperature=0.3,
)

llm_groq_1 = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=os.environ["GROQ_API_KEY"],
)

llm_groq_2 = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=os.environ["GROQ_API_KEY"],
)
LLM_POOL = [llm_google_1, llm_google_2, llm_google_3, llm_cohere, llm_groq_1, llm_groq_2]

def invoke_with_fallback(llms, messages):
    last_error = None

    for llm in llms:
        try:
            response = llm.invoke(messages)
            return response.content

        except Exception as e:
            last_error = e
            logging.warning(f"LLM failed: {llm} → {e}")

    raise RuntimeError("All LLMs failed") from last_error