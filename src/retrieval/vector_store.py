import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks() -> list[dict]:
    """Load all chunk files from the chunks directory."""

    chunks = []

    for json_path in sorted(CHUNKS_DIR.glob("*.json")):
        with json_path.open("r", encoding="utf-8") as file:
            file_chunks = json.load(file)

        chunks.extend(file_chunks)

    return chunks


def build_vector_store():
    """Create and persist the Chroma vector database."""

    print("Loading chunks...")
    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks.")

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    print("Creating embeddings...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
    )

    print("Creating Chroma database...")

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR)
    )

    collection_name = "ai_compliance_documents"

    try:
        client.delete_collection(
            name=collection_name
        )
        print("Existing Chroma collection deleted.")
    
    except Exception:
        print("No existing Chroma collection found.")

    collection = client.create_collection(
        name=collection_name
    )

    print("Adding documents to Chroma...")

    collection.add(
        ids=[chunk["chunk_id"] for chunk in chunks],
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "document_id": chunk["document_id"],
                "document_name": chunk["document_name"],
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ],
    )

    print("\nVector store created successfully.")
    print(f"Collection size: {collection.count()}")


if __name__ == "__main__":
    build_vector_store()