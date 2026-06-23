# rerank.py

import json
from datetime import datetime

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

DOCUMENT_FILE = "document_embeddings.json"
QUERY_FILE = "query_embeddings.json"


def get_embedding(text):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def save_query_embedding(query):

    try:
        with open(QUERY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    except:
        data = []

    record = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "embedding": get_embedding(query)
    }

    data.append(record)

    with open(QUERY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    return record


def cosine_similarity(v1, v2):

    v1 = np.array(v1)
    v2 = np.array(v2)

    return np.dot(v1, v2) / (
        np.linalg.norm(v1) * np.linalg.norm(v2)
    )


def rank_query(query):

    query_record = save_query_embedding(query)

    with open(DOCUMENT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    results = []

    for doc_name, doc_data in documents.items():

        score = cosine_similarity(
            query_record["embedding"],
            doc_data["embedding"]
        )

        results.append({
            "document": doc_name,
            "score": round(float(score) * 100, 2)
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results