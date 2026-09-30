import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.retrieval.page_chunker import create_page_chunks


PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


for json_path in sorted(PROCESSED_DATA_DIR.glob("*.json")):
    with json_path.open("r", encoding="utf-8") as file:
        pages = json.load(file)

    chunks = create_page_chunks(
        pages,
        chunk_size=2000,
        overlap=200,
    )

    print(f"\n{'=' * 80}")
    print(json_path.name)
    print(f"{'=' * 80}")
    print(f"Pages: {len(pages)}")
    print(f"Chunks: {len(chunks)}")

    if chunks:
        print("\nFirst chunk metadata:")
        print(chunks[0])

        print("\nLast chunk metadata:")
        print(chunks[-1])