"""Data loading module main script."""

from pathlib import Path
from typing import Any

from utils.path_utils import resolve_ancestor_directory
from data_loading.utils.txt_io import read_txt

RAW_TEXT_PATH = "raw_text_path"


def load_data(data_loading_config: dict[str, Any]) -> str:
    """Data load main module.

    Reads the input txt and returns the string version of it.

    Args:
        data_loading_config: Configuration of the data loading module.

    Returns:
        A string containing the full input text.
    """
    project_root = resolve_ancestor_directory(
        caller_file = Path(__file__),
        parent_levels=3,
    )

    relative_iput_file_path = data_loading_config[RAW_TEXT_PATH]

    return read_txt(
        file_path=project_root / relative_iput_file_path,
    )
