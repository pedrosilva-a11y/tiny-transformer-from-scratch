"""Test for Path utilities."""

import unittest
from pathlib import Path

from utils.path_utils import resolve_ancestor_directory

CURRENT_LEVEL_FOLDER = "utils"
ROOT_PARENT_LEVEL = 3
ROOT_LEVEL_FOLDER = "tiny-transformer-from-scratch"


class TestPathUtils(unittest.TestCase):
    """Test for Path Ancestor Resolution Utilities."""
    current_file_path: Path
    available_levels: int

    @classmethod
    def setUpClass(cls) -> None:
        """Runs once before all tests in this suite."""
        cls.current_file_path = Path(__file__).resolve()
        cls.available_levels = len(cls.current_file_path.parents)

    def test_root_level_ancestor_resolution(self) -> None:
        """Check if the resolved parent level is the root directory."""
        root_ancestor = resolve_ancestor_directory(
            caller_file=self.current_file_path,
            parent_levels=ROOT_PARENT_LEVEL,
        )

        self.assertIsInstance(root_ancestor, Path)
        self.assertEqual(root_ancestor.name, ROOT_LEVEL_FOLDER)

    def test_one_level_ancestor_resolution(self) -> None:
        """Check if the resolved parent for one level is correct."""
        root_ancestor = resolve_ancestor_directory(
            caller_file=self.current_file_path,
            parent_levels=1,
        )

        # This should be direct directory of the script.
        self.assertIsInstance(root_ancestor, Path)
        self.assertEqual(root_ancestor.name, CURRENT_LEVEL_FOLDER)

    def test_parent_level_argument_lower_than_one(self) -> None:
        """Check if ValueError is raised for values lower than one of parent_levels."""
        parent_levels = [0, -1, -2]

        expected_message = (
            "The parents are 1-indexed. "
            "Provide a value higher than 0."
        )

        for level in parent_levels:
            with self.assertRaises(ValueError) as context:
                resolve_ancestor_directory(
                    caller_file=self.current_file_path,
                    parent_levels=level,
                )

            self.assertEqual(str(context.exception), expected_message)

    def test_parent_level_argument_exceeds_maximum(self) -> None:
        """Check if ValueError is raised for values higher than the number of directories."""
        with self.assertRaises(ValueError) as context:
            resolve_ancestor_directory(
                caller_file=self.current_file_path,
                parent_levels=self.available_levels + 1,
            )

        expected_message = (
            "The function can step up "
            f"a maximum of {self.available_levels} levels."
        )

        self.assertEqual(str(context.exception), expected_message)


if __name__ == "__main__":
    unittest.main()
