from pathlib import Path

# from src.ingestion.pdf_loader import extract_text_from_pdf
from pdf_loader import extract_text_from_pdf

RAW_DATA_DIR = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
)


pdf_files = sorted(RAW_DATA_DIR.glob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError(
        f"No PDF files found in {RAW_DATA_DIR}"
    )


for pdf_path in pdf_files:
    pages = extract_text_from_pdf(str(pdf_path))

    print("\n" + "=" * 80)
    print(f"Document: {pdf_path.name}")
    print(f"Pages extracted: {len(pages)}")
    print("=" * 80)

    for page in pages[:2]:
        print(f"\nPage {page['page_number']}")
        print("-" * 40)
        print(page["text"][:500])