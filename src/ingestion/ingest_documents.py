import json
from pathlib import Path

from pdf_loader import extract_text_from_pdf
from text_cleaner import clean_text


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def main():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(RAW_DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {RAW_DATA_DIR}"
        )

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")

        pages = extract_text_from_pdf(str(pdf_path))

        for page in pages:
            page["text"] = clean_text(page["text"])

        output_path = (
            PROCESSED_DATA_DIR
            / f"{pdf_path.stem}.json"
        )

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(
                pages,
                file,
                ensure_ascii=False,
                indent=2,
            )

        print(
            f"Saved {len(pages)} pages → "
            f"{output_path.name}"
        )


if __name__ == "__main__":
    main()