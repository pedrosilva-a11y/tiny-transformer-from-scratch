"""Data loading module main script."""

from pathlib import Path

from data_loading.utils.txt_io import read_txt
from orchestration.schema import DataLoadingConfig
from utils.path_utils import resolve_ancestor_directory


def load_data(data_loading_config: DataLoadingConfig) -> str:
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

    relative_iput_file_path = data_loading_config.raw_text_path

    return read_txt(
        file_path=project_root / relative_iput_file_path,
    )
