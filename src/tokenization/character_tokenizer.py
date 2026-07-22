"""Character tokenizer methods."""


def character_frequency_mapping(raw_text: str) -> dict[str, int]:
    """Calculate the frequency profile of characters in the raw text.

    Args:
        raw_text: Loaded raw text corpus to process.

    Returns:
        A dictionary mapping input characters to their total occurrence counts.

    Raises:
        TypeError: If the raw_text input is not a string.
        ValueError: If the raw_text input is empty.
    """
    if not isinstance(raw_text, str):
        raise TypeError("The raw_text input should be a string.")

    if not raw_text:
        raise ValueError("Input should not be an empty string.")

    frequency_mapping: dict[str, int] = {}

    for char in raw_text:
        frequency_mapping[char] = frequency_mapping.get(char, 0) + 1

    return frequency_mapping
