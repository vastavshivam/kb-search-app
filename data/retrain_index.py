import sqlite3
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
from myconn import get_db;

# Load feedback
# conn = sqlite3.connect("feedback.db")
# cursor = conn.cursor()

# Select only relevant feedback
conn, cursor = get_db()
cursor.execute("SELECT complaint, response FROM feedback WHERE relevant = 1")
rows = cursor.fetchall()
conn.close()

# Combine for retraining (customize if needed)
texts = [row[0] + " " + row[1] for row in rows]

# Vectorize
model = SentenceTransformer('all-MiniLM-L6-v2')
vectors = model.encode(texts)

# Create new FAISS index
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors))

# Save index
faiss.write_index(index, "vector_index.index")
with open("feedback_texts.pkl", "wb") as f:
    pickle.dump(texts, f)
