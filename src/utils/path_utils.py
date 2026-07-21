"""Utilities for resolving ancestor directories from file paths."""

from pathlib import Path


def resolve_ancestor_directory(
    caller_file: str | Path,
    parent_levels: int,
) -> Path:
    """Resolve an ancestor directory relative to a caller file.

    Args:
        caller_file: File path used as the starting point, typically ``__file__``.
        parent_levels: Number of directory levels to move upward, using one-based
            counting. A value of 1 returns the file's containing directory, while
            a value of 2 returns the directory above it.

    Returns:
        Absolute path to the requested ancestor directory.

    Raises:
        ValueError: If ``parent_levels`` is less than 1 or exceeds the available
            number of ancestor directories.
    """
    if parent_levels < 1:
        raise ValueError(
            "The parents are 1-indexed. Provide a value higher than 0.",
        )

    absolute_path = Path(caller_file).resolve()
    total_levels = len(absolute_path.parents)

    if parent_levels > total_levels:
        raise ValueError(
            f"The function can step up a maximum of {total_levels} levels.",
        )

    return absolute_path.parents[parent_levels - 1]
