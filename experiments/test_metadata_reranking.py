import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DB_DIR = "vector_db"
COLLECTION_NAME = "ai_compliance_documents"

METADATA_PENALTY = 0.15


def is_metadata_chunk(chunk: dict) -> bool:
    text = chunk["text"].strip()

    if len(text) < 100:
        return True

    metadata_patterns = [
        "this publication is available free of charge from:",
        "artificial intelligence risk management framework (ai rmf 1.0)",
        "ai rmf ai rmf playbook playbook",
    ]

    text_lower = text.lower()

    return any(pattern in text_lower for pattern in metadata_patterns)


def retrieve(query: str, top_k: int = 5, candidate_k: int = 10):
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    query_embedding = model.encode([query])[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_k,
    )

    candidates = []

    for i in range(len(results["documents"][0])):
        chunk = {
            "text": results["documents"][0][i],
            "document_name": results["metadatas"][0][i]["document_name"],
            "page_number": results["metadatas"][0][i]["page_number"],
            "chunk_id": results["ids"][0][i],
            "distance": results["distances"][0][i],
        }

        adjusted_distance = chunk["distance"]

        if is_metadata_chunk(chunk):
            adjusted_distance += METADATA_PENALTY

        chunk["adjusted_distance"] = adjusted_distance
        candidates.append(chunk)

    candidates.sort(key=lambda x: x["adjusted_distance"])

    return candidates[:top_k]


QUESTIONS = [
    "What is the purpose of the NIST AI Risk Management Framework?",
    "What are the four core functions of the NIST AI Risk Management Framework?",
    "What is the purpose of the NIST Generative AI Profile?",
    "What does the NIST AI RMF Playbook provide?",
    "What requirements apply to high-risk AI systems under the EU AI Act?",
    "What AI practices are prohibited under the EU AI Act?",
    "What does the EU AI Act say about risk management for high-risk AI systems?",
]


def main():
    for question in QUESTIONS:
        print("\n" + "=" * 80)
        print("QUERY:", question)
        print("=" * 80)

        results = retrieve(question)

        for rank, result in enumerate(results, start=1):
            print(f"\n--- Result {rank} ---")
            print("Source:", result["document_name"])
            print("Page:", result["page_number"])
            print("Original distance:", round(result["distance"], 4))
            print("Adjusted distance:", round(result["adjusted_distance"], 4))
            print("Metadata chunk:", is_metadata_chunk(result))
            print("Chunk ID:", result["chunk_id"])
            print("\n", result["text"][:500])


if __name__ == "__main__":
    main()