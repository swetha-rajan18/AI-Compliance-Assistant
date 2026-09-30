def create_fixed_chunks(
    text: str,
    chunk_size: int = 2000,
    overlap: int = 200,
) -> list[str]:
    """
    Split text into overlapping fixed-size character chunks.

    Args:
        text: Input text.
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of characters shared between neighboring chunks.

    Returns:
        A list of text chunks.
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

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks