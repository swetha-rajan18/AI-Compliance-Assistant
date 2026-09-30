from pathlib import Path

from src.ingestion.pdf_loader import extract_text_from_pdf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def test_pdf_loader_returns_pages():
    pdf_path = RAW_DATA_DIR / "nist_ai_rmf_1.0.pdf"

    pages = extract_text_from_pdf(str(pdf_path))

    assert len(pages) > 0


def test_pdf_page_contains_required_metadata():
    pdf_path = RAW_DATA_DIR / "nist_ai_rmf_1.0.pdf"

    pages = extract_text_from_pdf(str(pdf_path))

    first_page = pages[0]

    assert "document_id" in first_page
    assert "document_name" in first_page
    assert "page_number" in first_page
    assert "text" in first_page


def test_pdf_page_metadata_is_correct():
    pdf_path = RAW_DATA_DIR / "nist_ai_rmf_1.0.pdf"

    pages = extract_text_from_pdf(str(pdf_path))

    first_page = pages[0]

    assert first_page["document_id"] == "nist_ai_rmf_1.0"
    assert first_page["document_name"] == "nist_ai_rmf_1.0.pdf"
    assert first_page["page_number"] == 1
    assert isinstance(first_page["text"], str)