def create_page_chunks(
    pages: list[dict],
    chunk_size: int = 2000,
    overlap: int = 200,
) -> list[dict]:
    """
    Create chunks independently within each PDF page.

    Each chunk retains the source document and page metadata.
    """

    if not isinstance(pages, list):
        raise TypeError("pages must be a list")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    for page in pages:
        text = page.get("text", "").strip()

        if not text:
            continue

        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": (
                            f"{page['document_id']}_"
                            f"p{page['page_number']}_"
                            f"c{chunk_index}"
                        ),
                        "document_id": page["document_id"],
                        "document_name": page["document_name"],
                        "page_number": page["page_number"],
                        "chunk_index": chunk_index,
                        "text": chunk_text,
                    }
                )

                chunk_index += 1

            if end >= len(text):
                break

            start = end - overlap

    return chunks