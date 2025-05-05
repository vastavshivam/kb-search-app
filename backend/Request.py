from fastapi import FastAPI, Request
from pydantic import BaseModel
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json

app = FastAPI()

# Load dataset and model
with open("cleaned_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("free_faiss_index.index")

# Greeting keywords
greetings = {"hi", "hello", "hey", "good morning", "good evening"}

# Chat request model
class ChatRequest(BaseModel):
    message: str
    state: str = "initial"  # state can be: initial, waiting_for_issue

@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.strip().lower()

    if req.state == "initial":
        if any(word in msg for word in greetings):
            return {
                "reply": "Hello! How can I assist you today?",
                "state": "waiting_for_issue"
            }
        else:
            return process_query(req.message)

    elif req.state == "waiting_for_issue":
        return process_query(req.message)

def process_query(query):
    # Embed and search
    query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")
    D, I = index.search(query_embedding, 3)

    results = []
    for score, idx in zip(D[0], I[0]):
        similarity = 1 / (1 + score)
        if similarity < 0.5:
            continue
        ticket = data[idx]
        results.append({
            "ticket_id": ticket.get("ticket_id"),
            "complaint": ticket.get("complaint_text"),
            "response": ticket.get("response_text"),
            "similarity": round(similarity, 2)
        })

    if results:
        return {
            "reply": f"Here’s what I found:\n\n{results[0]['response']}",
            "state": "waiting_for_issue"
        }
    else:
        return {
            "reply": "Thanks for sharing. I’ll forward this to our support team for further assistance.",
            "state": "waiting_for_issue"
        }
