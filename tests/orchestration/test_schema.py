"""Unit tests for the experiment configuration validation schema."""

import unittest
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from orchestration.schema import ExperimentConfig

RAW_TEXT_PATH = Path("data/raw/input.txt")


class TestExperimentConfigSchema(unittest.TestCase):
    """Verify schema parsing boundaries and configuration constraints."""

    valid_payload: dict[str, Any]

    def setUp(self) -> None:
        """Create a fresh valid payload before each test."""
        self.valid_payload = {
            "data_loading": {
                "raw_text_path": str(RAW_TEXT_PATH),
            },
        }

    def _assert_validation_error(
        self,
        payload: dict[str, Any],
        expected_location: tuple[str, ...],
        expected_type: str,
    ) -> None:
        """Assert that a payload produces one expected validation error.

        Args:
            payload: Raw configuration payload to validate.
            expected_location: Expected location of the invalid field.
            expected_type: Expected Pydantic validation error type.
        """
        with self.assertRaises(ValidationError) as context:
            ExperimentConfig.run_validation(payload)

        errors = context.exception.errors()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["loc"], expected_location)
        self.assertEqual(errors[0]["type"], expected_type)

    def test_valid_payload_is_parsed(self) -> None:
        """Parse a complete payload into a typed experiment configuration."""
        config = ExperimentConfig.run_validation(self.valid_payload)

        self.assertIsInstance(config, ExperimentConfig)
        self.assertIsInstance(config.data_loading.raw_text_path, Path)
        self.assertEqual(
            config.data_loading.raw_text_path,
            RAW_TEXT_PATH,
        )

    def test_missing_data_loading_section_is_rejected(self) -> None:
        """Reject a payload without the required data-loading section."""
        self.valid_payload.pop("data_loading")

        self._assert_validation_error(
            payload=self.valid_payload,
            expected_location=("data_loading",),
            expected_type="missing",
        )

    def test_missing_raw_text_path_is_rejected(self) -> None:
        """Reject a data-loading section without its required text path."""
        self.valid_payload["data_loading"].pop("raw_text_path")

        self._assert_validation_error(
            payload=self.valid_payload,
            expected_location=("data_loading", "raw_text_path"),
            expected_type="missing",
        )

    def test_extra_top_level_field_is_rejected(self) -> None:
        """Reject an undeclared top-level configuration field."""
        self.valid_payload["extra_key"] = "should_not_exist"

        self._assert_validation_error(
            payload=self.valid_payload,
            expected_location=("extra_key",),
            expected_type="extra_forbidden",
        )

    def test_extra_nested_field_is_rejected(self) -> None:
        """Reject an undeclared field inside the data-loading section."""
        self.valid_payload["data_loading"]["extra_key"] = "should_not_exist"

        self._assert_validation_error(
            payload=self.valid_payload,
            expected_location=("data_loading", "extra_key"),
            expected_type="extra_forbidden",
        )

    def test_invalid_raw_text_path_type_is_rejected(self) -> None:
        """Reject a raw-text path value that cannot be parsed as a path."""
        self.valid_payload["data_loading"]["raw_text_path"] = 1

        self._assert_validation_error(
            payload=self.valid_payload,
            expected_location=("data_loading", "raw_text_path"),
            expected_type="path_type",
        )


if __name__ == "__main__":
    unittest.main()
