import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.rag.rag_pipeline import RAGPipeline


def normalize_text(text: str) -> set[str]:
    """
    Convert text into a set of normalized words.

    Words shorter than four characters are ignored.
    """

    words = re.findall(
        r"\b[a-zA-Z]{4,}\b",
        text.lower(),
    )

    return set(words)


def calculate_evidence_overlap(
    answer: str,
    evidence: str,
) -> float:
    """
    Calculate the proportion of meaningful answer words
    that also appear in the cited evidence.

    This is a lexical heuristic, not a true semantic
    groundedness metric.
    """

    answer_words = normalize_text(answer)
    evidence_words = normalize_text(evidence)

    if not answer_words:
        return 0.0

    overlap = answer_words.intersection(
        evidence_words
    )

    return len(overlap) / len(answer_words)


def get_cited_evidence(
    retrieved_chunks: list[dict],
    source_numbers: list[int],
) -> str:
    """
    Return only the retrieved chunks corresponding to the
    source numbers cited by the LLM.
    """

    cited_chunks = []

    for source_number in source_numbers:

        index = source_number - 1

        if index < 0 or index >= len(retrieved_chunks):
            continue

        cited_chunks.append(
            retrieved_chunks[index]["text"]
        )

    return "\n".join(cited_chunks)


def main():

    rag = RAGPipeline()

    questions = [
        "What is the purpose of the NIST AI Risk Management Framework?",
        "What are the four core functions of the NIST AI Risk Management Framework?",
        "What does the EU AI Act require regarding post-market monitoring for certain high-risk AI systems?",
    ]

    for question in questions:

        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")
        print("=" * 80)

        # Generate the actual RAG answer.
        result = rag.answer(
            question,
            top_k=5,
        )

        answer = result["answer"]
        citations = result["citations"]

        print("\nANSWER:")
        print(answer)

        print("\nCITATIONS:")

        if citations:
            for citation in citations:
                print(citation)
        else:
            print("No citations.")

        # Retrieve the same chunks used by the RAG pipeline.
        retrieved_chunks = rag.retriever.search(
            question,
            top_k=5,
        )

        # Extract the source numbers selected by the LLM.
        source_numbers = [
            citation["source_number"]
            for citation in citations
        ]

        # Evaluate only against the cited evidence.
        cited_evidence = get_cited_evidence(
            retrieved_chunks,
            source_numbers,
        )

        if not cited_evidence:
            print(
                "\nEvidence overlap score: N/A "
                "(no valid cited evidence)"
            )
            continue

        score = calculate_evidence_overlap(
            answer,
            cited_evidence,
        )

        print(
            f"\nCited evidence overlap score: "
            f"{score:.4f}"
        )


if __name__ == "__main__":
    main()

