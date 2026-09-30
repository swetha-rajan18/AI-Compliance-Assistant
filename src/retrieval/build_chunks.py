import json
from pathlib import Path

from page_chunker import create_page_chunks


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"


def main():
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    total_chunks = 0

    for json_path in sorted(PROCESSED_DATA_DIR.glob("*.json")):
        with json_path.open("r", encoding="utf-8") as file:
            pages = json.load(file)

        chunks = create_page_chunks(
            pages,
            chunk_size=2000,
            overlap=200,
        )

        output_path = CHUNKS_DIR / json_path.name

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(
                chunks,
                file,
                ensure_ascii=False,
                indent=2,
            )

        print(
            f"{json_path.name}: "
            f"{len(chunks)} chunks → {output_path}"
        )

        total_chunks += len(chunks)

    print(f"\nTotal chunks: {total_chunks}")


if __name__ == "__main__":
    main()