import json
from pathlib import Path

# from src.retrieval.chunker import create_fixed_chunks
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.retrieval.chunker import create_fixed_chunks

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


for json_path in sorted(PROCESSED_DATA_DIR.glob("*.json")):
    with json_path.open("r", encoding="utf-8") as file:
        pages = json.load(file)

    full_text = "\n\n".join(
        page["text"]
        for page in pages
        if page["text"].strip()
    )

    chunks = create_fixed_chunks(
        full_text,
        chunk_size=2000,
        overlap=200,
    )

    print(f"\n{'=' * 80}")
    print(json_path.name)
    print(f"{'=' * 80}")
    print(f"Characters: {len(full_text):,}")
    print(f"Chunks: {len(chunks):,}")

    if chunks:
        print("\nFirst chunk:")
        print(chunks[0][:1000])

        print("\nLast chunk:")
        print(chunks[-1][:1000])