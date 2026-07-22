"""Tests for the character-level tokenizer."""

import re
import unittest
from pathlib import Path

from tokenization.character_tokenizer import character_frequency_mapping


class TestCharacterFrequencyMapping(unittest.TestCase):
    """Test the character-frequency mapping function."""

    def test_correct_mapping_result(self) -> None:
        """Return the expected occurrence count for each character."""
        input_string = "abacadaeafagahaiajakalamanaoapaqarasatauavawaxayaz"

        frequency_mapping = character_frequency_mapping(raw_text=input_string)

        expected_output_map = {
            "a": 25, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1,
            "i": 1, "j": 1, "k": 1, "l": 1, "m": 1, "n": 1, "o": 1, "p": 1,
            "q": 1, "r": 1, "s": 1, "t": 1, "u": 1, "v": 1, "w": 1, "x": 1,
            "y": 1, "z": 1,
        }

        self.assertIsInstance(frequency_mapping, dict)
        self.assertEqual(frequency_mapping, expected_output_map)

    def test_raise_error_for_non_string_input(self) -> None:
        """Raise TypeError for representative non-string inputs."""
        non_string_inputs = [
            None,
            {"a": 1},
            {"a", "b"},
            ("a", 1),
            ["a", 1],
            1,
            1.0,
            True,
            b"abc",
            Path("input.txt"),
        ]

        expected_message = "The raw_text input should be a string."
        # Escape special characters and anchor the pattern to enforce a exact string match
        expected_pattern = rf"^{re.escape(expected_message)}$"

        for raw_input in non_string_inputs:
            with (
                self.subTest(raw_input=repr(raw_input)),
                self.assertRaisesRegex(
                    TypeError,
                    expected_pattern
                ),
            ):
                character_frequency_mapping(raw_text=raw_input)  # type: ignore[arg-type]

    def test_raise_error_for_empty_inputs(self) -> None:
        """Raise ValueError for an empty string."""
        empty_input = ""

        with self.assertRaises(ValueError) as context:
            character_frequency_mapping(raw_text=empty_input)

        expected_message = "Input should not be an empty string."
        self.assertEqual(expected_message, str(context.exception))


if __name__ == "__main__":
    unittest.main()
