import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

DOCUMENTS_DIR = "documents"
OUTPUT_FILE = "document_embeddings.json"


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def main():
    embeddings = {}

    for file in Path(DOCUMENTS_DIR).glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        embeddings[file.name] = {
            "embedding": get_embedding(content)
        }

        print(f"Embedded {file.name}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(embeddings, f)

    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()