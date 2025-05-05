from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# Load cleaned dataset
with open("cleaned_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract complaint texts for embedding
texts = [item["complaint_text"] for item in data]

# Load SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, "free_faiss_index.index")

# Save full data (with ticket_id, complaint_text, response_text, etc.)
with open("free_ticket_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Indexed {len(texts)} complaints with full metadata retained.")


# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# import json

# # Load data
# with open("cleaned_dataset.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# texts = [item["input"] for item in data]
# responses = [item["output"] for item in data]

# # Load free embedding model
# model = SentenceTransformer('all-MiniLM-L6-v2')  # small & fast

# # Generate embeddings
# embeddings = model.encode(texts, convert_to_numpy=True)

# # Build FAISS index
# dimension = embeddings.shape[1]
# index = faiss.IndexFlatL2(dimension)
# index.add(embeddings)

# # Save index and responses
# faiss.write_index(index, "free_faiss_index.index")
# with open("free_responses.json", "w", encoding="utf-8") as f:
#     json.dump(responses, f, indent=2, ensure_ascii=False)

# print(f"✅ Indexed {len(texts)} complaints with free embeddings.")
