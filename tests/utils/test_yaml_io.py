"""Test for YAML IO utilities."""

import unittest
from pathlib import Path
from typing import Any

import yaml

from utils.yaml_io import read_yaml

ENCODING = "utf-8"
FIXTURES_CORRUPTED = "corrupted.yaml"
FIXTURES_DIR = "fixtures"
FIXTURES_EMPTY = "empty.yaml"
FIXTURE_HAPPY = "happy.yaml"
FIXTURE_NON_DICTIONARY = "non_dictionary.yaml"
FIXTURE_NON_STRING_KEY = "non_string_key.yaml"
FIXTURE_SYNTAX_ERROR = "syntax_error.yaml"

class TestYamlIo(unittest.TestCase):
    """Test for YAML reading utilities."""
    corrupted_file: Path
    empty_file: Path
    fixtures_dir: Path
    happy_file: Path
    non_dictionary_file: Path
    non_string_key_file: Path
    syntax_error_file: Path

    @classmethod
    def setUpClass(cls) -> None:
        """Runs once before all tests in this suite."""
        current_test_dir = Path(__file__).resolve().parent

        cls.fixtures_dir = current_test_dir / FIXTURES_DIR
        cls.fixtures_dir.mkdir(exist_ok=True)

        cls.happy_file = cls.fixtures_dir / FIXTURE_HAPPY

        cls.non_dictionary_file = cls.fixtures_dir / FIXTURE_NON_DICTIONARY

        cls.non_string_key_file = cls.fixtures_dir / FIXTURE_NON_STRING_KEY

        cls.syntax_error_file = cls.fixtures_dir / FIXTURE_SYNTAX_ERROR
        cls.syntax_error_file.write_text(
            "invalid_mapping: {\n  broken_indent: [missing_brackets\n",
            encoding=ENCODING,
        )

        cls.empty_file = cls.fixtures_dir / FIXTURES_EMPTY

        cls.corrupted_file = cls.fixtures_dir / FIXTURES_CORRUPTED
        cls.corrupted_file.write_bytes(b"\x80\x81\x82")

    @classmethod
    def _cleanup_files(cls, file_paths: list[Path]) -> None:
        """Helper to safely unlink a list of file paths if they exist.

        Args:
            file_paths: List of Path objects to be deleted.
        """
        for path in file_paths:
            if path.exists():
                path.unlink()

    @classmethod
    def tearDownClass(cls) -> None:
        """Runs once after all tests in this suite."""
        fixtures_to_delete = [
            cls.corrupted_file,
            cls.empty_file,
            cls.happy_file,
            cls.non_dictionary_file,
            cls.non_string_key_file,
            cls.syntax_error_file,
        ]
        cls._cleanup_files(file_paths=fixtures_to_delete)

        if cls.fixtures_dir.exists():
            cls.fixtures_dir.rmdir()

    def _create_yaml(
        self,
        yaml_content: Any,
        yaml_path: str | Path,
    ) -> None:
        """Helper to create yaml files.

        Args:
            yaml_content: Content to populate the yaml file.
            yaml_path: Path of the yaml to be created.
        """
        path = Path(yaml_path)
        with path.open(mode="w", encoding=ENCODING) as file:
            yaml.dump(
                yaml_content,
                file,
                default_flow_style=False,
                sort_keys=False,
            )

    def test_read_yaml_reads_yaml_as_dictionary(self) -> None:
        """Read a valid YAML as a dictionary."""
        happy_example = {
            "module_1": {
                "parameter_1": 1,
                "parameter_2": 2,
            },
            "module_2": {
                "parameter_3": 3,
                "parameter_4": 4,
            },
            "experiment_name": "test_yaml_read",
        }

        self._create_yaml(
            yaml_content=happy_example,
            yaml_path=self.happy_file,
        )

        actual = read_yaml(file_path=self.happy_file)
        self.assertEqual(actual, happy_example)
        self.assertIsInstance(actual, dict)
        self.assertTrue(
            all(isinstance(k, str) for k in actual),
        )

    def test_read_yaml_raises_file_not_found_error(self) -> None:
        """Raise FileNotFoundError for non-existing files."""
        missing_file = self.fixtures_dir / "non-existing.yaml"

        with self.assertRaises(FileNotFoundError) as context:
            read_yaml(file_path=missing_file)

        actual_message = str(context.exception)
        expected_message = f"The file at '{missing_file.resolve()}' does not exist."
        self.assertEqual(actual_message, expected_message)

    def test_read_yaml_raises_value_error_for_non_dictionaries(self) -> None:
        """Raises ValueError for non-dictionaries YAMLs."""
        non_dictionary_content = ["module_1", "parameter_1", "paramter_2"]

        self._create_yaml(
            yaml_content=non_dictionary_content,
            yaml_path=self.non_dictionary_file,
        )

        with self.assertRaises(ValueError) as context:
            read_yaml(file_path=self.non_dictionary_file)

        actual_message = str(context.exception)
        expected_message = (
            f"YAML file must contain a top-level mapping: "
            f"'{self.non_dictionary_file.name}'"
        )
        self.assertEqual(actual_message, expected_message)

    def test_read_yaml_raises_value_error_for_non_string_keys(self) -> None:
        """Raises ValueError for dictionaries with non-string keys."""
        non_string_key_dictionary = {
            1: {
                "parameter_1": 1,
                "parameter_2": 2,
            },
            2: {
                "parameter_3": 3,
                "parameter_4": 4,
            },
        }

        self._create_yaml(
            yaml_content=non_string_key_dictionary,
            yaml_path=self.non_string_key_file,
        )

        with self.assertRaises(ValueError) as content:
            read_yaml(file_path=self.non_string_key_file)

        actual_message = str(content.exception)
        expected_message = (
            f"YAML file top-level keys must all be strings: "
            f"'{self.non_string_key_file.name}'"
        )
        self.assertEqual(actual_message, expected_message)

    def test_read_yaml_raises_value_error_for_invalid_syntax(self) -> None:
        """Raises ValueError when YAML file contains invalid syntax."""
        with self.assertRaises(ValueError) as context:
            read_yaml(file_path=self.syntax_error_file)

        actual_message = str(context.exception)
        expected_prefix = f"Invalid YAML syntax in '{self.syntax_error_file.name}':"

        self.assertTrue(
            actual_message.startswith(expected_prefix),
        )

    def test_read_yaml_raises_value_error_for_empty_file(self) -> None:
        """Raises ValueError when YAML file is empty."""
        self.empty_file.write_text("", encoding=ENCODING)

        with self.assertRaises(ValueError) as context:
            read_yaml(file_path=self.empty_file)

        actual_message = str(context.exception)
        expected_message = f"YAML file is empty: '{self.empty_file.name}'"
        self.assertEqual(actual_message, expected_message)

    def test_read_yaml_raises_value_error_for_corrupted_file(self) -> None:
        """Raise ValueError when corrupted files throws UnicodeDecodeError."""
        with self.assertRaises(ValueError) as context:
            read_yaml(file_path=self.corrupted_file)

        actual_message = str(context.exception)
        expected_message = (
            f"Could not decode '{self.corrupted_file.name}' "
            f"using encoding '{ENCODING}'."
        )
        self.assertEqual(actual_message, expected_message)


if __name__ == "__main__":
    unittest.main()
