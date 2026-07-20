"""
backend_sqlite.py
=================

Part 1 - Foundation

Contains:
    ✔ Gemini LLM
    ✔ MCP Tool Loading
    ✔ SQLite Checkpointer
    ✔ Chat State
    ✔ Title Generator
    ✔ Helper Functions

Graph creation will be done in Part 2.
"""

import asyncio
import sqlite3
from typing import Annotated, TypedDict

from dotenv import load_dotenv

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    BaseMessage,
)
from langchain_core.prompts import ChatPromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

from mcp_tools.client import get_tools


# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()


# ============================================================
# Gemini Model
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
)


# ============================================================
# Load MCP Tools
# ============================================================

print("=" * 60)
print("Loading MCP Tools...")
print("=" * 60)

TOOLS = asyncio.run(get_tools())

print(f"Loaded {len(TOOLS)} MCP Tool(s):")

for tool in TOOLS:
    print(f"   • {tool.name}")

print("=" * 60)


# ============================================================
# Bind Tools to Gemini
# ============================================================

llm = llm.bind_tools(TOOLS)


# ============================================================
# SQLite Checkpointer
# ============================================================

checkpoint_connection = sqlite3.connect(
    "chatbot.db",
    check_same_thread=False,
)

memory = SqliteSaver(checkpoint_connection)


# ============================================================
# Chat State
# ============================================================

class ChatState(TypedDict):
    """
    LangGraph State
    """

    messages: Annotated[list[BaseMessage], add_messages]


# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """
You are a helpful AI assistant.

You have access to external MCP tools.

Rules:

1. If a tool is required, ALWAYS use it.
2. Never guess mathematical calculations.
3. Be concise.
4. Explain your reasoning after receiving tool results.
5. If no tool is needed, answer normally.
"""


# ============================================================
# Chat Title Generator
# ============================================================

title_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Generate a short title for this conversation.

Rules:

- Maximum 5 words.
- No punctuation.
- No quotes.
- Return ONLY the title.
""",
        ),
        ("human", "{message}"),
    ]
)

title_chain = title_prompt | llm


def generate_chat_title(first_message: str) -> str:
    """
    Generate a short conversation title.
    """

    try:

        response = title_chain.invoke(
            {
                "message": first_message
            }
        )

        return response.content.strip()

    except Exception:

        return "New Chat"


# ============================================================
# Helper Functions
# ============================================================

def get_last_human_message(messages: list[BaseMessage]) -> str:
    """
    Returns the latest HumanMessage content.
    """

    for message in reversed(messages):

        if isinstance(message, HumanMessage):
            return message.content

    return ""


def get_last_ai_message(messages: list[BaseMessage]) -> str:
    """
    Returns the latest AIMessage content.
    """

    for message in reversed(messages):

        if isinstance(message, AIMessage):
            return message.content

    return ""


# ============================================================
# Placeholder
# ============================================================

"""
Part 2 will add:

- async chat_node()
- Tool execution
- Routing
- LangGraph workflow
"""