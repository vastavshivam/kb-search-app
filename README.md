# 🤖 AppG Customer Support Chatbot

A smart AI-powered chatbot built with FastAPI and Streamlit that helps customers get instant responses to their complaints by matching them with previous resolved tickets using vector similarity search (FAISS + Sentence Transformers).

---

## 🚀 Features

- 🔍 Semantic search using SentenceTransformers & FAISS
- 📚 Uses historical support data to provide accurate suggestions
- 💬 Supports small talk (e.g., "What is your name?")
- 🌐 Web frontend built with Streamlit
- ⚡ FastAPI backend API
- 📦 Easy deployment on Render or other cloud platforms

---

## 🏗️ Project Structure

kb-search-app/ │ ├── backend/ │ ├── main.py # FastAPI app │ ├── utils.py # Helper functions (embedding, search) │ ├── data/ │ │ ├── free_faiss_index.index │ │ └── free_ticket_data.json │ ├── frontend/ │ └── app.py # Streamlit frontend app │ ├── cleaned_dataset.json # Original dataset (input/output pairs) ├── requirements.txt # Python dependencies └── README.md # Project documentation
---

## 🧠 How It Works

- When a user submits a complaint, the backend converts it into an embedding using a SentenceTransformer model (`all-MiniLM-L6-v2`).
- The FAISS index finds the closest historical complaint.
- The system returns the best-matched complaint and its associated response.
- If the query matches a small-talk phrase (like "what is your name?"), the system responds conversationally.

---

## 🛠️ Local Setup

