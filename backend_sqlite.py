import os
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.graph.message import add_messages

from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# for mcp
# import asyncio
# from mcp_tools.client import get_tools
# from langgraph.prebuilt import ToolNode,tools_condition
# from langgraph.graph import MessagesState



load_dotenv()

# ------------------------------------------------------------------
# LLM
# ------------------------------------------------------------------

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


# ---------------------------------------------------------
# MCP Tool Loading
# ---------------------------------------------------------

# TOOLS = asyncio.run(get_tools())
# tool_node = ToolNode(TOOLS)

# ------------------------------------------------------------------
# Graph State
# ------------------------------------------------------------------

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ------------------------------------------------------------------
# Chat Node
# ------------------------------------------------------------------

def chat_node(state: ChatState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# def chat_node(state: ChatState):
#     """LLM node that may answer or request a tool call."""
#     response = llm.bind_tools(TOOLS).invoke(state["messages"])

#     return {
#         "messages": [response]
#     }

# ------------------------------------------------------------------
# Conversation Title Generator
# ------------------------------------------------------------------

def generate_chat_title(first_message: str) -> str:
    """
    Generates a short 2-3 word title from the user's first message.
    """

    prompt = f"""
You are an AI that creates very short conversation titles.

Rules:
- Maximum 2 or 3 words.
- No punctuation.
- No quotation marks.
- No emojis.
- Return ONLY the title.
- Make it descriptive.

User Message:
{first_message}
"""

    try:
        response = llm.invoke(prompt)
        title = response.content.strip()

        # Safety cleanup
        title = title.replace('"', "").replace("'", "")

        # Keep at most first 3 words
        words = title.split()
        title = " ".join(words[:3])

        return title if title else "New Chat"

    except Exception:
        return "New Chat"


# ------------------------------------------------------------------
# Checkpointer and database integration
# ------------------------------------------------------------------
conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)


# ------------------------------------------------------------------
# Build Graph
# ------------------------------------------------------------------



# graph = StateGraph(ChatState)

# graph.add_node("chat_node", chat_node)
# graph.add_node("tools", tool_node)

# graph.add_edge(START, "chat_node")

# graph.add_conditional_edges(
#     "chat_node",
#     tools_condition,
#     {
#         "tools": "tools",
#         "__end__": END,
#     },
# )

# graph.add_edge("tools", "chat_node")

# chatbot = graph.compile(checkpointer=checkpointer)
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)



def retrieve_all_threads():

    all_threads = []

    seen = set()

    for checkpoint in checkpointer.list(None):

        thread_id = checkpoint.config["configurable"]["thread_id"]

        if thread_id not in seen:

            seen.add(thread_id)

            all_threads.append(
                {
                    "id": thread_id,
                    "title": "New Chat"
                }
            )

    return all_threads