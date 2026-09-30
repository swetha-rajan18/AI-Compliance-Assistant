import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.rag.rag_pipeline import RAGPipeline


rag = RAGPipeline()


question = "What does the EU AI Act say about risk management for high-risk AI systems?"

result = rag.answer(
    question,
    top_k=5,
)

print("\n" + "=" * 80)
print("QUESTION")
print("=" * 80)
print(result["question"])

print("\n" + "=" * 80)
print("ANSWER")
print("=" * 80)
print(result["answer"])

print("\n" + "=" * 80)
print("CITATIONS")
print("=" * 80)

for citation in result["citations"]:
    print(
        f"- {citation['document']} "
        f"| Page {citation['page']} "
        f"| {citation['chunk_id']}"
    )