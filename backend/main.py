from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Initialize FastAPI
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
INDEX_PATH = os.path.join(ROOT_DIR, "data", "free_faiss_index.index")
DATA_PATH = os.path.join(ROOT_DIR, "data", "free_ticket_data.json")
model = SentenceTransformer('all-MiniLM-L6-v2')
# index = faiss.read_index("../data/free_faiss_index.index")
index = faiss.read_index(INDEX_PATH)

# Load dataset
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare texts and responses
complaint_texts = [d["complaint_text"] for d in data]
responses = [d["response_text"] for d in data]

# Define greetings
greetings = {"hi", "hello", "hey", "good morning", "good evening"}



# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handle small talk / static questions
SMALL_TALK_RESPONSES = {
    "what is your name ?": "Hello! I'm AppG, your virtual assistant here to help with support-related queries.",
    "who are you ?": "I'm AppG, your helpful support assistant.",
    "hi": "Hi there! How can I help you today?",
    "hello": "Hello! I’m AppG. What can I assist you with?",
    "how are you": "I'm just a bot, but I'm always ready to help!"
}

# Request model
class ChatRequest(BaseModel):
    message: str
    state: str = "initial"  # "initial" or "waiting_for_issue"

# Search API (optional)
@app.get("/search")
def search_tickets(query: str = Query(..., description="Complaint text"), top_k: int = 3):
    embedding = model.encode([query], convert_to_numpy=True).astype("float32")
    D, I = index.search(embedding, top_k)

    results = []
    for score, idx in zip(D[0], I[0]):
        similarity = 1 / (1 + score)
        results.append({
            "ticket_id": data[idx]["ticket_id"],
            "complaint": data[idx]["complaint_text"],
            "response": data[idx]["response_text"],
            "similarity": round(similarity, 2)
        })

    return {"query": query, "results": results}

# Chat API
@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.strip().lower()
    print (msg)

    if req.state == "initial":
        if any(greet in msg for greet in greetings):
            return {
                "reply": "Hello! How can I assist you today?",
                "state": "waiting_for_issue"
            }
        elif msg in SMALL_TALK_RESPONSES:
            print ("elif is true")
            return {                
                "reply": SMALL_TALK_RESPONSES[msg],
                "state": "waiting_for_issue",                
                
        }
        else:
            return process_query(req.message)

    elif req.state == "waiting_for_issue":
        return process_query(req.message)

def process_query(query):
    embedding = model.encode([query], convert_to_numpy=True).astype("float32")
    D, I = index.search(embedding, 3)

    results = []
    for score, idx in zip(D[0], I[0]):
        similarity = 1 / (1 + score)
        if similarity < 0.5:
            continue
        ticket = data[idx]
        results.append({
            "ticket_id": ticket["ticket_id"],
            "complaint": ticket["complaint_text"],
            "response": ticket["response_text"],
            "similarity": float(round(similarity, 2))
        })
        # print(results)

    if results:
        return {
            "reply": f"Here’s what I found:\n\n{results[0]['response']}",
            "state": "waiting_for_issue",
            "results": results
        }
    else:
        return {
            "reply": "Thanks for sharing. I’ll forward this to our support team for further assistance.",
            "state": "waiting_for_issue",
            "results": []
        }

# Entry point to run app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# from fastapi import FastAPI, Query
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# import json
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn
# from pydantic import BaseModel

# # Load model & FAISS index
# model = SentenceTransformer('all-MiniLM-L6-v2')
# index = faiss.read_index("../data/free_faiss_index.index")

# # Load original data
# with open("../data/cleaned_dataset.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# greetings = {"hi", "hello", "hey", "good morning", "good evening"} # i f any greeting comes 
# responses = [d["output"] for d in data]

# # Init FastAPI app
# app = FastAPI()

# class ChatRequest(BaseModel):
#     message: str
#     state: str = "initial"  # state can be: initial, waiting_for_issue

# # Allow frontend to call backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/search")
# def search_tickets(query: str = Query(..., description="Complaint text"), top_k: int = 3):
#     embedding = model.encode([query], convert_to_numpy=True)
#     D, I = index.search(embedding, top_k)

#     results = []
#     for idx in I[0]:
#         results.append({
#             "similar_complaint": texts[idx],
#             "suggested_response": responses[idx]
#         })
#     return {"query": query, "results": results}

# @app.post("/chat")
# def chat(req: ChatRequest):
#     msg = req.message.strip().lower()

#     if req.state == "initial":
#         if any(word in msg for word in greetings):
#             return {
#                 "reply": "Hello! How can I assist you today?",
#                 "state": "waiting_for_issue"
#             }
#         else:
#             return process_query(req.message)

#     elif req.state == "waiting_for_issue":
#         return process_query(req.message)

# def process_query(query):
#     # Embed and search
#     query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")
#     D, I = index.search(query_embedding, 3)

#     results = []
#     for score, idx in zip(D[0], I[0]):
#         similarity = 1 / (1 + score)
#         if similarity < 0.5:
#             continue
#         ticket = data[idx]
#         results.append({
#             "ticket_id": ticket.get("ticket_id"),
#             "complaint": ticket.get("complaint_text"),
#             "response": ticket.get("response_text"),
#             "similarity": round(similarity, 2)
#         })

#     if results:
#         return {
#             "reply": f"Here’s what I found:\n\n{results[0]['response']}",
#             "state": "waiting_for_issue"
#         }
#     else:
#         return {
#             "reply": "Thanks for sharing. I’ll forward this to our support team for further assistance.",
#             "state": "waiting_for_issue"
#         }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)




