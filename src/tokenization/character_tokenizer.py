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


def sort_and_extract_tokens(
    frequency_mapping: dict[str, int],
) -> list[str]:
    """Extract character tokens in deterministic Unicode order.

    Args:
        frequency_mapping: Characters mapped to their occurrence counts.

    Returns:
        A list of characters sorted in deterministic Unicode order.

    Raises:
        TypeError: If the input is not a dictionary.
        TypeError: If a key is not a string.
        TypeError: If a value is not an integer.
        ValueError: If the mapping is empty.
    """
    if not isinstance(frequency_mapping, dict):
        raise TypeError("The frequency_mapping input should be a dictionary.")

    if not frequency_mapping:
        raise ValueError("Input should not be an empty dictionary.")

    if not all(isinstance(key, str) for key in frequency_mapping):
        raise TypeError("All keys in the mapping must be strings.")

    if not all(
        type(value) is int
        for value in frequency_mapping.values()
    ):
        raise TypeError("All values in the mapping must be integers.")

    return sorted(frequency_mapping)
