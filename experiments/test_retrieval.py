import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.retrieval.retriever import Retriever
retriever = Retriever()


queries = [
    "What is the purpose of the NIST AI Risk Management Framework?",
    "What are the requirements for high-risk AI systems?",
    "What does the EU AI Act say about prohibited AI practices?",
]


for query in queries:
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retriever.search(
        query,
        top_k=5,
    )

    for rank, result in enumerate(results, start=1):
        print(f"\n--- Result {rank} ---")
        print(
            f"Source: {result['document_name']} "
            f"| Page: {result['page_number']}"
        )
        print(f"Distance: {result['distance']:.4f}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"\n{result['text'][:700]}...")