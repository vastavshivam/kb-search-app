import json
import random
from sentence_transformers import SentenceTransformer, util


# Input and output file paths
input_file = "free_ticket_data.json"
output_file = "mistral_finetune.jsonl"

# Variants for user prompts
USER_PROMPT_TEMPLATES = [
    "What is the status of ticket ID {ticket_id}?",
    "Can you give me an update on ticket {ticket_id}?",
    "What's going on with ticket number {ticket_id}?",
    "Please provide the latest update for ticket {ticket_id}.",
    "I want to know the current status of ticket {ticket_id}.",
    "Give me the update on ticket ID {ticket_id}.",
    "Could you check ticket {ticket_id} for me?",
    "Has there been any progress on ticket {ticket_id}?",
    "Update me on ticket ID {ticket_id}.",
    "What’s the progress on ticket number {ticket_id}?"
]

# Load JSON data
with open(input_file, "r", encoding="utf-8") as f:
    records = json.load(f)
count = 0
# Open JSONL output file
with open(output_file, "w", encoding="utf-8") as out:
    for record in records:
        ticket_id = record.get("ticket_id", "").strip()
        response = record.get("response_text", "").strip()
        complaint= record.get("complaint_text", "").strip()
   
        print (record['complaint_text'])
        if ticket_id and response and "complaint_text" in record:
            prompt_variants = random.sample(USER_PROMPT_TEMPLATES, k=3)
            
            
            for user_prompt_template in prompt_variants:
                user_query = user_prompt_template.format(ticket_id=ticket_id)

                messages = [
                    { "role": "system", "content": "You are a helpful support assistant that answers ticket queries based on ticket_id." },
                    { "role": "user", "content": user_query },
                    { "role": "assistant", "content": response }
                ]
                out.write(json.dumps({"messages": messages}) + "\n")
                count += 1

            
            messages = [
                {"role": "system", "content": "You are a helpful support assistant."},
                {"role": "user", "content": f"Complaint: {record['complaint_text']}"},
                {"role": "assistant", "content": record["response_text"]}
            ]
            out.write(json.dumps({"messages": messages}) + "\n")
            count += 1


print(f"✅ Converted {count} valid records to {output_file}")



# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load JSONL file
embeddings = []
with open("mistral_finetune.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        messages = data.get("messages", [])

        # Extract the user message
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), None)
        
        if user_msg:
            emb = model.encode(user_msg)
            embeddings.append((user_msg, emb))

# Print example
print(f"Total messages encoded: {len(embeddings)}")
print("Sample vector:\n", embeddings[0][1])


