import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"


def main():

    chunks = []

    for json_path in sorted(CHUNKS_DIR.glob("*.json")):
        with json_path.open("r", encoding="utf-8") as file:
            chunks.extend(json.load(file))

    lengths = [
        len(chunk["text"])
        for chunk in chunks
    ]

    print(f"Total chunks: {len(lengths)}")

    for threshold in [50, 100, 150, 200, 250, 300]:

        count = sum(
            length < threshold
            for length in lengths
        )

        print(
            f"Chunks shorter than {threshold} characters: "
            f"{count}"
        )


if __name__ == "__main__":
    main()