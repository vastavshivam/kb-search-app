import json

# Load your raw JSON file
with open("customer_support_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Create a clean dataset
cleaned_data = []

for ticket in raw_data:
    complaint_text = ticket.get("complaint_text", "").strip()
    response_text = ticket.get("response_text", "").strip()
    ticket_id = ticket.get("ticket_id", "").strip()

    if complaint_text and response_text:
        cleaned_data.append({
            "ticket_id": ticket_id,
            "complaint_text": complaint_text,
            "response_text": response_text
        })

# Save the cleaned data
with open("cleaned_dataset.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

print(f"✅ Cleaned {len(cleaned_data)} records saved to 'cleaned_dataset.json'")



# import json
# import pandas as pd

# # Load your raw JSON file (can also be a list of dicts directly)
# with open("customer_support_data.json", "r", encoding="utf-8") as f:
#     raw_data = json.load(f)

# # Create a clean dataset
# cleaned_data = []

# for ticket in raw_data:
#     complaint_text = ticket.get("complaint_text", "").strip()
#     response_text = ticket.get("response_text", "").strip()
#     ticket_id=ticket.get("ticket_id","").strip()
#     complaint= ticket.get("complaint_text","").strip()
            
            
    
#     if complaint_text and response_text:
#         cleaned_data.append({
#             "input": complaint_text,
#             "output": response_text
#         })

# # Save the cleaned data for fine-tuning or embedding
# with open("cleaned_dataset.json", "w", encoding="utf-8") as f:
#     json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

# print(f"Cleaned {len(cleaned_data)} records saved to 'cleaned_dataset.json'")
