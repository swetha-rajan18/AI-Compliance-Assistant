import re


def clean_text(text: str) -> str:
    """
    Clean text extracted from a PDF while preserving its meaning.

    Args:
        text: Raw text extracted from a PDF page.

    Returns:
        Cleaned text.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Fix words broken across PDF line breaks.
    # Example:
    # recommenda-
    # tion
    # becomes:
    # recommendation
    text = re.sub(r"-\s*\n\s*", "", text)

    # Replace remaining line breaks with spaces.
    text = re.sub(r"\s*\n\s*", " ", text)

    # Collapse repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()