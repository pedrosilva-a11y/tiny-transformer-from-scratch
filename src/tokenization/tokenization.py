"""Tokenizer main script."""

from tokenization.character_tokenizer import character_frequency_mapping


def build_tokens(raw_input: str) -> dict[str, int]:
    """Run the token setup.

    Args:
        raw_input: Loaded raw text corpus to process.

    Returns:
        A dictionary mapping input characters to their total occurrence counts.
    """
    return character_frequency_mapping(raw_text=raw_input)
