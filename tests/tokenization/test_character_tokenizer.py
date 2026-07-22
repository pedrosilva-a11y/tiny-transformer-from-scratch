"""Tests for the character-level tokenizer."""

import re
import unittest
from pathlib import Path
from typing import Any

from tokenization.character_tokenizer import (
    character_frequency_mapping,
    sort_and_extract_tokens,
)


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
        non_string_inputs: list[Any] = [
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
        # Escape special characters and anchor the pattern to enforce an exact match.
        expected_pattern = rf"^{re.escape(expected_message)}$"

        for raw_input in non_string_inputs:
            with (
                self.subTest(raw_input=repr(raw_input)),
                self.assertRaisesRegex(
                    TypeError,
                    expected_pattern
                ),
            ):
                character_frequency_mapping(raw_text=raw_input)

    def test_raise_error_for_empty_inputs(self) -> None:
        """Raise ValueError for an empty string."""
        empty_input = ""

        with self.assertRaises(ValueError) as context:
            character_frequency_mapping(raw_text=empty_input)

        expected_message = "Input should not be an empty string."
        self.assertEqual(expected_message, str(context.exception))


class TestSortAndExtractTokens(unittest.TestCase):
    """Verify character token sorting and boundary constraint validation rules."""

    def _assert_validation_error(
        self,
        payload: Any,
        expected_exception: type[Exception],
        expected_message: str,
    ) -> None:
        """Assert that an input raises the expected exception and message.

        Args:
            payload: Raw input configuration to validate.
            expected_exception: The specific exception class type to catch.
            expected_message: The exact literal error message phrase expected.
        """
        with self.assertRaises(expected_exception) as context:
            sort_and_extract_tokens(frequency_mapping=payload)

        self.assertEqual(expected_message, str(context.exception))

    def test_should_successfully_extract_and_sort_tokens(self) -> None:
        """Ensure a mixed frequency map returns a fresh, alphabetically sorted list of tokens."""
        frequency_mapping = {
            "b": 2, "\n": 4, "A": 1, "!": 3, "a": 5, " ": 8,
        }

        sorted_keys = sort_and_extract_tokens(frequency_mapping=frequency_mapping)

        expected_keys = [
            "\n", " ", "!", "A", "a","b",
        ]

        self.assertIsInstance(sorted_keys, list)
        self.assertEqual(sorted_keys, expected_keys)

    def test_should_reject_non_dictionary_inputs(self) -> None:
        """Ensure non-dictionary inputs trigger an immediate type error."""
        non_dictionary_inputs: list[Any] = [
            None,
            "a",
            {"a", "b"},
            ("a", 1),
            ["a", 1],
            1,
            1.0,
            True,
            b"abc",
            Path("input.txt"),
        ]

        expected_message = "The frequency_mapping input should be a dictionary."
        # Escape special characters and anchor the pattern to enforce an exact match.
        expected_pattern = rf"^{re.escape(expected_message)}$"

        for input_value in non_dictionary_inputs:
            with(
                self.subTest(inputs=repr(input_value)),
                self.assertRaisesRegex(
                    TypeError,
                    expected_pattern,
                ),
            ):
                sort_and_extract_tokens(frequency_mapping=input_value)

    def test_should_reject_empty_dictionary(self) -> None:
        """Ensure an empty frequency dictionary drops execution with a value error."""
        empty_mapping: dict[Any, Any] = {}

        self._assert_validation_error(
            payload=empty_mapping,
            expected_exception=ValueError,
            expected_message="Input should not be an empty dictionary.",
        )

    def test_should_reject_non_string_keys(self) -> None:
        """Ensure keys that are not primitive strings fail validation."""
        non_string_keys = {"A": 1500, 1: 2, "B": 3}

        self._assert_validation_error(
            payload=non_string_keys,
            expected_exception=TypeError,
            expected_message="All keys in the mapping must be strings.",
        )

    def test_should_reject_non_integer_values(self) -> None:
        """Ensure character frequencies that are not integers fail validation."""
        non_integer_values = {"A": 1500, "B": 3, "C": 3, "D": True}

        self._assert_validation_error(
            payload=non_integer_values,
            expected_exception=TypeError,
            expected_message="All values in the mapping must be integers.",
        )


if __name__ == "__main__":
    unittest.main()
