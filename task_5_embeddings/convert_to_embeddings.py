from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

descriptions = [
    "I want to do what is good, but I don't. I don't want to do what is wrong, but I do it anyway",
    "Here's something that might reframe how you think about the hard seasons: sometimes what feels like loss is actually pruning."
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=descriptions
)

documents = []

for idx, (text, item) in enumerate(zip(descriptions, response.data), start=1):
    documents.append({
        "id": idx,
        "description": text,
        "embedding_model": "text-embedding-3-small",
        "embedding_dimension": len(item.embedding),
        "embedding": item.embedding,
        "created_at": datetime.utcnow().isoformat()
    })

with open("embeddings.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2)

print("Saved embeddings.json")