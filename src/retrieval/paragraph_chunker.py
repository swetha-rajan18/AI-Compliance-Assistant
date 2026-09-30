def create_paragraph_chunks(
    text: str,
    chunk_size: int = 2000,
    overlap: int = 200,
) -> list[str]:
    """
    Create chunks while attempting to preserve paragraph boundaries.

    Paragraphs are combined until adding another paragraph would exceed
    the target chunk size.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()

    if not text:
        return []

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_paragraphs = []
    current_length = 0

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)

        if (
            current_paragraphs
            and current_length + paragraph_length + 2 > chunk_size
        ):
            chunks.append("\n\n".join(current_paragraphs))

            # Keep the final paragraph as overlap.
            overlap_paragraph = current_paragraphs[-1]

            current_paragraphs = [overlap_paragraph]
            current_length = len(overlap_paragraph)

        current_paragraphs.append(paragraph)
        current_length += paragraph_length + 2

    if current_paragraphs:
        chunks.append("\n\n".join(current_paragraphs))

    return chunks