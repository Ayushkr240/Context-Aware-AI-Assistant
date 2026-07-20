# 🤖 Context-Aware AI Assistant

A context-aware AI assistant built using **LangGraph**, **Streamlit**, and **Google Gemini**, featuring persistent conversation memory and multi-threaded chat management.

---

## 📖 Overview

This project is an AI-powered conversational assistant designed to provide a seamless chatting experience with persistent conversation history. It leverages LangGraph to manage conversational workflows and SQLite for storing chat sessions, allowing users to continue previous conversations across application restarts.

This project is being developed as part of an **AI Project-Based Learning** course.

---

## ✨ Features

- 💬 Multi-threaded conversations
- 🧠 Persistent conversation memory
- 💾 SQLite-based chat persistence
- 📜 Conversation history recovery
- ✏️ AI-generated chat titles
- 📝 Rename chat threads
- 🗑️ Delete chat threads
- ⚡ Real-time streaming AI responses
- 🤖 Powered by Google Gemini
- 🎨 Clean Streamlit interface

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python
- LangGraph
- LangChain
- SQLite

### AI Model
- Google Gemini

---

## 📂 Project Structure

```text
CB/
│
├── backend_sqlite.py
├── frontend_sqlite.py
├── database.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Ayushkr240/Context-Aware-AI-Assistant.git 
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

### 5. Run the application

```bash
streamlit run frontend_sqlite.py
```

---

## 📸 Screenshots

> Add screenshots of the application here.

---

## 🔄 Future Improvements

- 🔌 Model Context Protocol (MCP) integration
- 📄 Document Q&A using RAG
- 🌐 Web search tools
- 🎤 Voice interaction
- 🖼️ Image understanding
- 🤖 Multi-agent workflows
- 📅 Calendar and productivity tools

---

## 👨‍💻 Author

**Ayush Kumar**

GitHub: https://github.com/Ayushkr240

---

## 📄 License

This project is developed for educational purposes as part of an AI Project.
