"""Download the Tiny Shakespeare dataset."""

from pathlib import Path
from urllib.request import Request, urlopen

DATA_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
ENCODING = "utf-8"
OUTPUT_PATH = Path("data/raw/input.txt")
REQUEST_HEADERS = {"User-Agent": "tiny-transformer-from-scratch"}
URL_TIMEOUT_SECONDS = 30


def main() -> None:
    """Download Tiny Shakespeare and save it as a local raw text file."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    request = Request(
        DATA_URL,
        headers=REQUEST_HEADERS,
    )

    with urlopen(request, timeout=URL_TIMEOUT_SECONDS) as response:
        text = response.read().decode(ENCODING)

    OUTPUT_PATH.write_text(text, encoding=ENCODING)

    print(f"Downloaded Tiny Shakespeare to {OUTPUT_PATH}")
    print(f"Characters: {len(text):,}")


if __name__ == "__main__":
    main()
