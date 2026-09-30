import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.retrieval.retriever import Retriever


QUESTIONS_FILE = PROJECT_ROOT / "evaluation" / "questions.json"


def load_questions():
    with QUESTIONS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_question(retriever, item, top_k=5):
    question = item["question"]
    expected_documents = set(item["expected_documents"])

    results = retriever.search(
        question,
        top_k=top_k,
    )

    retrieved_documents = [
        result["document_name"]
        for result in results
    ]

    retrieved_documents_set = set(retrieved_documents)

    top_1_hit = (
        retrieved_documents[0] in expected_documents
        if expected_documents
        else None
    )
    
    if expected_documents:
        hit = bool(
            expected_documents.intersection(
                retrieved_documents_set
            )
        )
    else:
        hit = None

    return {
        "question": question,
        "expected_documents": list(expected_documents),
        "retrieved_documents": retrieved_documents,
        "distances": [
            round(result["distance"], 4)
            for result in results
        ],
        "best_distance": results[0]["distance"],
        "hit": hit,
        "top_1_hit": top_1_hit,
        "in_scope": bool(expected_documents),
    }

def main():
    questions = load_questions()
    retriever = Retriever()

    results = []

    for item in questions:
        print("\n" + "=" * 80)
        print(f"Question: {item['question']}")

        result = evaluate_question(
            retriever,
            item,
            top_k=5,
        )

        results.append(result)

        print(f"Expected: {result['expected_documents']}")
        print(f"Retrieved: {result['retrieved_documents']}")
        print(f"Best distance: {result['best_distance']:.4f}")
        print(f"Distances: {result['distances']}")

        if result["in_scope"]:
            print(f"Document hit: {result['hit']}")
        else:
            print("Out-of-scope question")

    in_scope_results = [
        result for result in results
        if result["in_scope"]
    ]

    out_of_scope_results = [
        result for result in results
        if not result["in_scope"]
    ]

    in_scope_hits = sum(
        result["hit"]
        for result in in_scope_results
    )

    top_1_hits = sum(
        result["top_1_hit"]
        for result in in_scope_results
    )

    print("\n" + "=" * 80)
    print("RETRIEVAL EVALUATION SUMMARY")
    print("=" * 80)

    print(
        f"In-scope questions: "
        f"{len(in_scope_results)}"
    )

    print(
        f"In-scope document hits: "
        f"{in_scope_hits}/{len(in_scope_results)}"
    )

    print(
        f"In-scope hit rate: "
        f"{in_scope_hits / len(in_scope_results):.2%}"
    )

    print(
        f"In-scope Recall@1: "
        f"{top_1_hits}/{len(in_scope_results)}"
    )

    print(
        f"Recall@1: "
        f"{top_1_hits / len(in_scope_results):.2%}"
    )

    print("\nOut-of-scope questions:")

    for result in out_of_scope_results:
        print(
            f"- {result['question']} "
            f"→ best distance: "
            f"{result['best_distance']:.4f}"
        )


if __name__ == "__main__":
    main()