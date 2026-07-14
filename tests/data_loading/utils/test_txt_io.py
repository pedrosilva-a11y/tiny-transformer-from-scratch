"""Test for TXT IO utilities."""

import unittest
from pathlib import Path

from data_loading.utils.txt_io import read_txt

CORRUPTED_FILE = "corrupted.txt"
ENCODING = "utf-8"
FIXTURES_DIR = "fixtures"
FIXTURE_HAPPY_FILE = "happy.txt"

class TestTxtIo(unittest.TestCase):
    """Tests for TXT reading utilities."""

    @classmethod
    def setUpClass(cls) -> None:
        """Runs once before all tests in this suite."""
        current_test_dir = Path(__file__).resolve().parent

        cls.fixtures_dir = current_test_dir / FIXTURES_DIR
        cls.fixtures_dir.mkdir(exist_ok=True)

        cls.happy_file = cls.fixtures_dir / FIXTURE_HAPPY_FILE
        cls.happy_file.write_text(
            "Camelot: By my troth, I shall test this right noble TXT reading function.",
            encoding=ENCODING,
        )

        cls.corrupted_file = cls.fixtures_dir / CORRUPTED_FILE
        cls.corrupted_file.write_bytes(
            b"\x80\x81\x82",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Runs once after all tests in this suite."""
        if cls.happy_file.exists():
            cls.happy_file.unlink()

        if cls.corrupted_file.exists():
            cls.corrupted_file.unlink()

        if cls.fixtures_dir.exists():
            cls.fixtures_dir.rmdir()

    def test_read_txt_reads_txt_file_as_string(self) -> None:
        """Read a valid TXT file as a string."""
        actual = read_txt(file_path=self.fixtures_dir / FIXTURE_HAPPY_FILE)
        expected = "Camelot: By my troth, I shall test this right noble TXT reading function."
        self.assertEqual(actual, expected)
        self.assertIsInstance(actual, str)


    def test_read_txt_raises_file_not_found_error(self) -> None:
        """Raise FileNotFoundError for non-existing files."""
        missing_file = self.fixtures_dir / "non_existing.txt"

        with self.assertRaises(FileNotFoundError) as context:
            read_txt(file_path=missing_file)

        actual_message = str(context.exception)
        expected_message = f"The file at '{missing_file}' does not exist."
        self.assertEqual(actual_message, expected_message)

    def test_read_txt_raises_value_error_for_corrupted_txt(self) -> None:
        """Raise ValueError when corrupted files throws UnicodeDecodeError."""
        with self.assertRaises(ValueError) as context:
            read_txt(file_path=self.corrupted_file)
        
        actual_message = str(context.exception)
        expected_message = (
            f"Could not decode '{self.corrupted_file.name}' "
            f"using encoding 'utf-8'."
        )
        self.assertEqual(actual_message, expected_message)


if __name__ == "__main__":
    unittest.main()
