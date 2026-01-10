# from langchain_core.chat_history import InMemoryChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
# from models import llm_groq
# from mongo import fetch_eda_data

# # In-memory store per run_id
CHAT_STORE = {}

def get_history(run_id: str):
    if run_id not in CHAT_STORE:
        CHAT_STORE[run_id] = InMemoryChatMessageHistory()
    return CHAT_STORE[run_id]


def initialize_memory(run_id: str):
    doc = fetch_eda_data(run_id)
    if not doc:
        raise ValueError("EDA data not found")

    history = get_history(run_id)

    history.add_message(
        HumanMessage(
            content=f"""
Dataset Overview:
{doc['llm_overview']}

EDA Insight Summary:
{doc['eda_summary']}
"""
        )
    )


# def chat_with_data(run_id: str, user_query: str) -> str:
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are a senior data scientist."),
#         ("placeholder", "{history}"),
#         ("human", "{input}")
#     ])

#     chain = prompt | llm_groq

#     runnable = RunnableWithMessageHistory(
#         chain,
#         lambda session_id: get_history(session_id),
#         input_messages_key="input",
#         history_messages_key="history",
#     )

#     response = runnable.invoke(
#         {"input": user_query},
#         config={"configurable": {"session_id": run_id}}
#     )

#     return response.content

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from Backend.models import llm_groq
from Backend.mongo import fetch_eda_data

# Global in-memory store
CHAT_STORE = {}

def chat_with_data(run_id: str, user_query: str) -> str:
    # 1️⃣ Create or fetch history
    if run_id not in CHAT_STORE:
        print(run_id)
        CHAT_STORE[run_id] = InMemoryChatMessageHistory()

        # Load EDA once
        doc = fetch_eda_data(run_id)
        if not doc:
            raise ValueError("EDA data not found for this run_id")

        CHAT_STORE[run_id].add_message(
            SystemMessage(
                content=f"""
                    You are a senior data scientist.
                    You already analyzed this dataset.

                    EDA SUMMARY:
                    {doc.get("eda_summary", "")}

                    DETAILED OVERVIEW:
                    {doc.get("llm_overview", "")}

                    Answer user questions ONLY using this information.
                    Do NOT ask for the dataset again.
                """
            )
        )
    print(run_id)
    history = CHAT_STORE[run_id]

    # 2️⃣ Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system}"),
        ("placeholder", "{history}"),
        ("human", "{input}")
    ])

    chain = prompt | llm_groq

    # 3️⃣ Runnable with history
    runnable = RunnableWithMessageHistory(
        chain,
        lambda _: history,
        input_messages_key="input",
        history_messages_key="history",
    )

    response = runnable.invoke(
        {
            "input": user_query,
            "system": "You are a senior data scientist."
        },
        config={"configurable": {"session_id": run_id}}
    )
    print(CHAT_STORE[run_id])
    return response.content
