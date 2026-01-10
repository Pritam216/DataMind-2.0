from langchain_cohere import ChatCohere
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# llm_google = ChatGoogleGenerativeAI(
#     model = "gemini-2.5-flash",
#     temperature = 0.3,
#     api_key = os.environ["GEMINI_API_KEY"],
# )

llm_google = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-lite",
    temperature = 0.3,
    api_key = os.environ["GEMINI_API_KEY"],
)

llm_cohere = ChatCohere(
    model="command-a-03-2025",
    temperature=0.3,
)

llm_groq = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=os.environ["GROQ_API_KEY"],
)
# llm_groq = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0.3,
#     api_key=os.environ["GROQ_API_KEY"],
# )

# response1=llm_google.invoke("Write about LLM in short")
# response2=llm_cohere.invoke("Write about LLM in short")
# response3=llm_groq.invoke("write about LLM in short")

# print(response1.content,"\n\n",response2.content,'\n\n',response3.content)
# print(response3.content)