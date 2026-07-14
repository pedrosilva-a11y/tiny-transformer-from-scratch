"""Utilities for reading TXT files."""

from pathlib import Path

ENCODING = "utf-8"

def read_txt(file_path: str | Path) -> str:
    """Read a TXT file as a string.

    Args:
        file_path: Path to the TXT file.

    Returns:
        String containing the TXT content.

    Raises:
        FileNotFoundError: If the target file does not exist.
        ValueError: If the file cannot be decoded using the specified encoding.
    """
    path = Path(file_path)

    try:
        with path.open(encoding=ENCODING) as file:
            return file.read()

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The file at '{path.resolve()}' does not exist.",
        ) from e

    except UnicodeDecodeError as e:
        raise ValueError(
            f"Could not decode '{path.name}' using encoding '{ENCODING}'.",
        ) from e
