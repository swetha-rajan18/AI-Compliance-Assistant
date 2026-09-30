from pathlib import Path

import pymupdf


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF page by page.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list of dictionaries containing document and page metadata.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document_id = pdf_path.stem
    document_name = pdf_path.name

    pages = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            pages.append(
                {
                    "document_id": document_id,
                    "document_name": document_name,
                    "page_number": page_number,
                    "text": text,
                }
            )

    return pages