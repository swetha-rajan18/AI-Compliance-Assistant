import sys
from pathlib import Path

from sentence_transformers import CrossEncoder


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.retrieval.retriever import Retriever


RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


EVALUATION_QUESTIONS = [
    {
        "question": "What is the purpose of the NIST AI Risk Management Framework?",
        "expected_documents": ["nist_ai_rmf_1.0.pdf"],
    },
    {
        "question": "What are the four core functions of the NIST AI Risk Management Framework?",
        "expected_documents": ["nist_ai_rmf_1.0.pdf"],
    },
    {
        "question": "What is the purpose of the NIST Generative AI Profile?",
        "expected_documents": ["nist_generative_ai_profile.pdf"],
    },
    {
        "question": "What does the NIST AI RMF Playbook provide?",
        "expected_documents": ["nist_ai_rmf_playbook.pdf"],
    },
    {
        "question": "What requirements apply to high-risk AI systems under the EU AI Act?",
        "expected_documents": ["eu_ai_act.pdf"],
    },
    {
        "question": "What AI practices are prohibited under the EU AI Act?",
        "expected_documents": ["eu_ai_act.pdf"],
    },
    {
        "question": "What does the EU AI Act say about risk management for high-risk AI systems?",
        "expected_documents": ["eu_ai_act.pdf"],
    },
]


def rerank_results(
    question: str,
    results: list[dict],
    reranker: CrossEncoder,
) -> list[dict]:
    """
    Rerank retrieved chunks using a cross-encoder.
    """

    pairs = [
        [question, result["text"]]
        for result in results
    ]

    scores = reranker.predict(pairs)

    reranked = []

    for result, score in zip(results, scores):
        result_copy = result.copy()
        result_copy["rerank_score"] = float(score)
        reranked.append(result_copy)

    reranked.sort(
        key=lambda item: item["rerank_score"],
        reverse=True,
    )

    return reranked


def main():

    print("Loading retriever...")
    retriever = Retriever()

    print("Loading cross-encoder reranker...")
    reranker = CrossEncoder(RERANKER_MODEL)

    baseline_top_1_hits = 0
    reranked_top_1_hits = 0

    baseline_top_5_hits = 0
    reranked_top_5_hits = 0

    print("\n" + "=" * 80)
    print("RERANKING EXPERIMENT")
    print("=" * 80)

    for item in EVALUATION_QUESTIONS:

        question = item["question"]
        expected_documents = set(
            item["expected_documents"]
        )

        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")
        print("=" * 80)

        # --------------------------------------------------
        # Stage 1: Existing semantic retrieval
        # --------------------------------------------------

        baseline_results = retriever.search(
            question,
            top_k=10,
        )

        baseline_top_1 = baseline_results[0]

        baseline_top_5_documents = {
            result["document_name"]
            for result in baseline_results[:5]
        }

        baseline_top_1_hit = (
            baseline_top_1["document_name"]
            in expected_documents
        )

        baseline_top_5_hit = bool(
            expected_documents.intersection(
                baseline_top_5_documents
            )
        )

        # --------------------------------------------------
        # Stage 2: Cross-encoder reranking
        # --------------------------------------------------

        reranked_results = rerank_results(
            question,
            baseline_results,
            reranker,
        )

        reranked_top_1 = reranked_results[0]

        reranked_top_5_documents = {
            result["document_name"]
            for result in reranked_results[:5]
        }

        reranked_top_1_hit = (
            reranked_top_1["document_name"]
            in expected_documents
        )

        reranked_top_5_hit = bool(
            expected_documents.intersection(
                reranked_top_5_documents
            )
        )

        if baseline_top_1_hit:
            baseline_top_1_hits += 1

        if baseline_top_5_hit:
            baseline_top_5_hits += 1

        if reranked_top_1_hit:
            reranked_top_1_hits += 1

        if reranked_top_5_hit:
            reranked_top_5_hits += 1

        print("\nBASELINE TOP 3:")

        for rank, result in enumerate(
            baseline_results[:3],
            start=1,
        ):
            print(
                f"{rank}. "
                f"{result['document_name']} | "
                f"page {result['page_number']} | "
                f"distance {result['distance']:.4f}"
            )

        print("\nRERANKED TOP 3:")

        for rank, result in enumerate(
            reranked_results[:3],
            start=1,
        ):
            print(
                f"{rank}. "
                f"{result['document_name']} | "
                f"page {result['page_number']} | "
                f"rerank score {result['rerank_score']:.4f}"
            )

    total = len(EVALUATION_QUESTIONS)

    print("\n" + "=" * 80)
    print("RERANKING EXPERIMENT SUMMARY")
    print("=" * 80)

    print(
        f"Baseline Recall@1: "
        f"{baseline_top_1_hits}/{total} "
        f"({baseline_top_1_hits / total:.2%})"
    )

    print(
        f"Reranked Recall@1: "
        f"{reranked_top_1_hits}/{total} "
        f"({reranked_top_1_hits / total:.2%})"
    )

    print(
        f"\nBaseline Recall@5: "
        f"{baseline_top_5_hits}/{total} "
        f"({baseline_top_5_hits / total:.2%})"
    )

    print(
        f"Reranked Recall@5: "
        f"{reranked_top_5_hits}/{total} "
        f"({reranked_top_5_hits / total:.2%})"
    )


if __name__ == "__main__":
    main()
