"""Experiment configuration validation schema."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class DataLoadingConfig(BaseModel):
    """Schema for the dataset ingestion and parsing configurations.
    
    File existence is checked by the Input/Output Operations.
    """
    raw_text_path: Path = Field(
        ...,
        description = "Repository-relative path to the raw text input file.",
    )

    model_config = {
        "extra": "forbid",
    }


class ExperimentConfig(BaseModel):
    """Pydantic configuration dictionary contract."""
    data_loading: DataLoadingConfig = Field(
        ...,
        description = "Ingestion configuration",
    )

    model_config = {
        "extra": "forbid",
    }

    @classmethod
    def run_validation(cls, config: dict[str, Any]) -> "ExperimentConfig":
        """Validate a raw configuration dictionary against the Pydantic schema.

        Args:
            config: Raw configuration dictionary parsed from YAML.

        Returns:
            ExperimentConfig: A validated instance of the configuration schema.
        """
        return cls.model_validate(config)
