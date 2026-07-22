"""Tokenizer main script."""

from tokenization.character_tokenizer import (
    character_frequency_mapping,
    create_token_id_mapping,
    sort_and_extract_tokens,
)


def build_tokens(raw_input: str) -> dict[str, int]:
    """Run the token setup.

    Args:
        raw_input: Loaded raw text corpus to process.

    Returns:
        A dictionary mapping each character to a unique sequential ID.
    """
    freq_mapping = character_frequency_mapping(raw_text=raw_input)

    extracted_sorted_tokens = sort_and_extract_tokens(
        frequency_mapping=freq_mapping,
    )

    return create_token_id_mapping(
        characters_sorted=extracted_sorted_tokens,
    )
