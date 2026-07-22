"""Tests for the character-level tokenizer."""

import re
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any

from tokenization.character_tokenizer import (
    character_frequency_mapping,
    create_token_id_mapping,
    sort_and_extract_tokens,
)


class TokenizerTestCase(unittest.TestCase):
    """Base test case providing shared assertions for character-tokenizer tests."""

    def _assert_raises_with_message(
        self,
        tested_function: Callable[..., Any],
        keyword_arguments: dict[str, Any],
        exception_type: type[Exception],
        exception_message: str,
    ) -> None:
        """Assert that an input raises the expected exception and message.

        Args:
            tested_function: Callable to execute and validate.
            keyword_arguments: Keyword arguments passed to the tested function.
            exception_type: The specific exception class type to catch.
            exception_message: The exact literal error message phrase expected.
        """
        with self.assertRaises(exception_type) as context:
            tested_function(**keyword_arguments)

        self.assertEqual(exception_message, str(context.exception))


class TestCharacterFrequencyMapping(TokenizerTestCase):
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
        arguments = {"raw_text": empty_input}

        self._assert_raises_with_message(
            tested_function=character_frequency_mapping,
            keyword_arguments=arguments,
            exception_type=ValueError,
            exception_message = "Input should not be an empty string."
        )


class TestSortAndExtractTokens(TokenizerTestCase):
    """Verify character token sorting and boundary constraint validation rules."""

    def test_should_successfully_extract_and_sort_tokens(self) -> None:
        """Ensure a mixed frequency map returns a fresh, Unicode-sorted list of tokens."""
        frequency_mapping = {
            "b": 2, "\n": 4, "A": 1, "!": 3, "a": 5, " ": 8,
        }

        sorted_keys = sort_and_extract_tokens(frequency_mapping=frequency_mapping)

        expected_keys = [
            "\n", " ", "!", "A", "a", "b",
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
            with (
                self.subTest(input_value=repr(input_value)),
                self.assertRaisesRegex(
                    TypeError,
                    expected_pattern,
                ),
            ):
                sort_and_extract_tokens(frequency_mapping=input_value)

    def test_should_reject_empty_dictionary(self) -> None:
        """Ensure an empty frequency dictionary drops execution with a value error."""
        empty_mapping: dict[Any, Any] = {}
        args = {"frequency_mapping": empty_mapping}

        self._assert_raises_with_message(
            tested_function=sort_and_extract_tokens,
            keyword_arguments=args,
            exception_type=ValueError,
            exception_message="Input should not be an empty dictionary.",
        )

    def test_should_reject_non_string_keys(self) -> None:
        """Ensure keys that are not primitive strings fail validation."""
        non_string_keys = {"A": 1500, 1: 2, "B": 3}
        args = {"frequency_mapping": non_string_keys}

        self._assert_raises_with_message(
            tested_function=sort_and_extract_tokens,
            keyword_arguments=args,
            exception_type=TypeError,
            exception_message="All keys in the mapping must be strings.",
        )

    def test_should_reject_non_integer_values(self) -> None:
        """Ensure character frequencies that are not integers fail validation."""
        non_integer_values = {"A": 1500, "B": 3, "C": 3, "D": True}
        args = {"frequency_mapping": non_integer_values}

        self._assert_raises_with_message(
            tested_function=sort_and_extract_tokens,
            keyword_arguments=args,
            exception_type=TypeError,
            exception_message="All values in the mapping must be integers.",
        )


class TestCreateTokenIdMapping(TokenizerTestCase):
    """Verify correct creation of the token id mapping."""

    def test_should_successfully_create_token_id(self) -> None:
        """Ensure a token ID mapping is correctly created."""
        sorted_list = ["\n", " ", "!", "A", "B", "C", "a", "d", "e"]
        expected_output = {
            "\n": 0, " ": 1, "!": 2, "A": 3, "B": 4, "C": 5, "a": 6,
            "d": 7, "e": 8,
        }

        token_id_mapping = create_token_id_mapping(
            characters_sorted=sorted_list,
        )

        self.assertIsInstance(token_id_mapping, dict)
        self.assertEqual(token_id_mapping, expected_output)


    def test_should_reject_non_list_inputs(self) -> None:
        """Ensure non-list inputs trigger an immediate type error."""
        non_list_inputs: list[Any] = [
            None,
            "a",
            {"a", "b"},
            ("a", 1),
            {"a": 1},
            1,
            1.0,
            True,
            b"abc",
            Path("input.txt"),
        ]

        expected_message = "The characters_sorted input should be a list."
        expected_pattern = rf"^{re.escape(expected_message)}$"

        for non_list in non_list_inputs:
            with (
                self.subTest(input_value=repr(non_list)),
                self.assertRaisesRegex(
                    TypeError,
                    expected_pattern,
                ),
            ):
                create_token_id_mapping(characters_sorted=non_list)

    def test_should_reject_empty_list(self) -> None:
        """Ensure an empty list drops execution with a value error."""
        args: dict[str, list] = {"characters_sorted": []}

        self._assert_raises_with_message(
            tested_function=create_token_id_mapping,
            keyword_arguments=args,
            exception_type=ValueError,
            exception_message="The characters_sorted input should not be empty.",
        )


    def test_should_reject_non_string_elements(self) -> None:
        """Ensure a list with at least one non-string elements is rejected with a type error."""
        args = {"characters_sorted": ["A", "B", "C", True, "z"]}

        self._assert_raises_with_message(
            tested_function=create_token_id_mapping,
            keyword_arguments=args,
            exception_type=TypeError,
            exception_message="All list elements should be strings.",
        )

    def test_should_reject_unsorted_input_lists(self) -> None:
        """Ensure an unsorted list is dropped with a value error."""
        args = {"characters_sorted": ["a", "A", "!", "\n"]}

        self._assert_raises_with_message(
            tested_function=create_token_id_mapping,
            keyword_arguments=args,
            exception_type=ValueError,
            exception_message="Input must be sorted.",
        )

    def test_should_reject_non_single_length_elements(self) -> None:
        """Reject strings not exactly one character long with a value error."""
        args = {"characters_sorted": ["A", "AA", "B", "C", "D", "a", "z"]}

        self._assert_raises_with_message(
            tested_function=create_token_id_mapping,
            keyword_arguments=args,
            exception_type=ValueError,
            exception_message="All list elements must be a single character.",
        )

    def test_should_reject_list_with_duplicates(self) -> None:
        """Reject lists with duplciates by raising a value error."""
        args = {"characters_sorted": ["A", "A", "B", "C", "z"]}

        self._assert_raises_with_message(
            tested_function=create_token_id_mapping,
            keyword_arguments=args,
            exception_type=ValueError,
            exception_message="The characters_sorted input must not contain duplicates.",
        )


if __name__ == "__main__":
    unittest.main()
