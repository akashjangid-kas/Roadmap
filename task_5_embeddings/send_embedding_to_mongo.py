from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Read MongoDB URI from .env
mongo_uri = os.getenv("MONGODB_URI")

if not mongo_uri:
    raise ValueError("MONGODB_URI is not set in .env")

# Connect to MongoDB
client = MongoClient(mongo_uri)

db = client["vector_db"]
collection = db["embeddings"]

# Load JSON file
with open("embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Insert documents
result = collection.insert_many(data)

print(f"Inserted {len(result.inserted_ids)} documents.")

