import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.retrieval.chunker import create_fixed_chunks
from src.retrieval.paragraph_chunker import create_paragraph_chunks


PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


for json_path in sorted(PROCESSED_DATA_DIR.glob("*.json")):
    with json_path.open("r", encoding="utf-8") as file:
        pages = json.load(file)

    full_text = "\n\n".join(
        page["text"]
        for page in pages
        if page["text"].strip()
    )

    fixed_chunks = create_fixed_chunks(
        full_text,
        chunk_size=2000,
        overlap=200,
    )

    paragraph_chunks = create_paragraph_chunks(
        full_text,
        chunk_size=2000,
        overlap=200,
    )

    print(f"\n{'=' * 80}")
    print(json_path.name)
    print(f"{'=' * 80}")

    print(f"Fixed-size chunks: {len(fixed_chunks)}")
    print(f"Paragraph chunks:  {len(paragraph_chunks)}")

    print("\n--- Fixed chunk boundary ---")
    print(fixed_chunks[0][-300:])
    print("\nNEXT:")
    print(fixed_chunks[1][:300])

    print("\n--- Paragraph chunk boundary ---")
    print(paragraph_chunks[0][-300:])
    print("\nNEXT:")
    print(paragraph_chunks[1][:300])