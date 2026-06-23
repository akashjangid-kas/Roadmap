import json
from datetime import datetime

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# ==========================================================
# EDIT YOUR QUERY HERE
# ==========================================================
QUERY = """
Machine Learning is a technique that allows computers to learn from data and make decisions without explicit programming
"""
# ==========================================================

load_dotenv()

client = OpenAI()

DOCUMENT_FILE = "document_embeddings.json"
QUERY_FILE = "query_embeddings.json"


def get_embedding(text):
    """
    Generate embedding using OpenAI text-embedding-3-small
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def save_query_embedding(query):
    """
    Save query embedding to query_embeddings.json

    If the latest stored query is identical,
    reuse the existing embedding instead of
    creating a new API call.
    """

    try:
        with open(QUERY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Reuse latest embedding if query is unchanged
    if data and data[-1]["query"].strip() == query.strip():
        print("Latest query already embedded. Reusing existing embedding.")
        return data[-1]

    print("Generating new query embedding...")

    record = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "embedding": get_embedding(query)
    }

    data.append(record)

    with open(QUERY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    print("Query embedding saved.")

    return record


def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity
    """

    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )


def rank_documents(query_embedding):
    """
    Compare query embedding against all document embeddings
    """

    with open(DOCUMENT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    results = []

    for doc_name, doc_data in documents.items():

        score = cosine_similarity(
            query_embedding,
            doc_data["embedding"]
        )

        results.append({
            "document": doc_name,
            "similarity": float(score)
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results


def main():

    query = QUERY.strip()

    if not query:
        print("QUERY string is empty.")
        return

    query_record = save_query_embedding(query)

    results = rank_documents(
        query_record["embedding"]
    )

    print("\n" + "=" * 70)
    print("QUERY")
    print("=" * 70)
    print(query)

    print("\n" + "=" * 70)
    print("DOCUMENT RANKINGS")
    print("=" * 70)

    for rank, result in enumerate(results, start=1):

        similarity_percent = result["similarity"] * 100

        print(
            f"{rank}. {result['document']}"
            f" | Score: {result['similarity']:.4f}"
            f" | Similarity: {similarity_percent:.2f}%"
        )


if __name__ == "__main__":
    main()