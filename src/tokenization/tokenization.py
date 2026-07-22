"""Tokenizer main script."""

from tokenization.character_tokenizer import (
    character_frequency_mapping,
    sort_and_extract_tokens,
)


def build_tokens(raw_input: str) -> list[str]:
    """Run the token setup.

    Args:
        raw_input: Loaded raw text corpus to process.

    Returns:
        A list of characters sorted in deterministic Unicode order.
    """
    freq_mapping = character_frequency_mapping(raw_text=raw_input)

    return sort_and_extract_tokens(frequency_mapping=freq_mapping)
