"""Download the Tiny Shakespeare dataset."""

from pathlib import Path
from urllib.request import Request, urlopen


DATA_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
OUTPUT_PATH = Path("data/raw/input.txt")


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    request = Request(
        DATA_URL,
        headers={"User-Agent": "tiny-transformer-from-scratch"},
    )

    with urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8")

    OUTPUT_PATH.write_text(text, encoding="utf-8")

    print(f"Downloaded Tiny Shakespeare to {OUTPUT_PATH}")
    print(f"Characters: {len(text):,}")


if __name__ == "__main__":
    main()
