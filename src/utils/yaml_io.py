"""Utilities for reading YAML files."""

from pathlib import Path
from typing import Any

import yaml

ENCODING = "utf-8"


def read_yaml(file_path: str | Path) -> dict[str, Any]:
    """Read a YAML file into a dictionary.

    Args:
        file_path: Path to the YAML file.

    Returns:
        Dictionary containing the YAML content.

    Raises:
        FileNotFoundError: If the target file does not exist.
        ValueError:
            If the file cannot be decoded using the specified encoding.
            If the YAML file is empty.
            If the YAML file is not a dictionary.
            If the YAML file contains non-string top-level keys.
            If the YAML file contains invalid syntax.
    """
    path = Path(file_path)

    try:
        with path.open(encoding=ENCODING) as file:
            read_data = yaml.safe_load(file)

        if read_data is None:
            raise ValueError(
                f"YAML file is empty: '{path.name}'",
            )

        if not isinstance(read_data, dict):
            raise ValueError(
                f"YAML file must contain a top-level mapping: '{path.name}'",
            )

        if not all(isinstance(k, str) for k in read_data):
            raise ValueError(
                f"YAML file top-level keys must all be strings: '{path.name}'",
            )

        return read_data

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The file at '{path.resolve()}' does not exist.",
        ) from e

    except UnicodeDecodeError as e:
        raise ValueError(
            f"Could not decode '{path.name}' using encoding '{ENCODING}'.",
        ) from e

    except yaml.YAMLError as e:
        raise ValueError(
            f"Invalid YAML syntax in '{path.name}': {e}",
        ) from e
