from pathlib import Path

import pymupdf
from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PDF_FILES = [
    RAW_DATA_DIR / "eu_ai_act.pdf",
    RAW_DATA_DIR / "nist_ai_rmf_playbook.pdf",
]


def test_with_pymupdf(pdf_path):
    print(f"\n{'=' * 80}")
    print(f"PyMuPDF: {pdf_path.name}")
    print(f"{'=' * 80}")

    with pymupdf.open(pdf_path) as document:
        for page_number in [0, 1]:
            text = document[page_number].get_text("text")

            print(f"\nPage {page_number + 1}")
            print(f"Characters extracted: {len(text)}")
            print(text[:300])


def test_with_pypdf(pdf_path):
    print(f"\n{'=' * 80}")
    print(f"pypdf: {pdf_path.name}")
    print(f"{'=' * 80}")

    reader = PdfReader(pdf_path)

    for page_number in [0, 1]:
        text = reader.pages[page_number].extract_text() or ""

        print(f"\nPage {page_number + 1}")
        print(f"Characters extracted: {len(text)}")
        print(text[:300])


for pdf_path in PDF_FILES:
    test_with_pymupdf(pdf_path)
    test_with_pypdf(pdf_path)
    