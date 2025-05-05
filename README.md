
---

## 🧠 How It Works

- When a user submits a complaint, the backend converts it into an embedding using a SentenceTransformer model (`all-MiniLM-L6-v2`).
- The FAISS index finds the closest historical complaint.
- The system returns the best-matched complaint and its associated response.
- If the query matches a small-talk phrase (like "what is your name?"), the system responds conversationally.

---

## 🛠️ Local Setup

