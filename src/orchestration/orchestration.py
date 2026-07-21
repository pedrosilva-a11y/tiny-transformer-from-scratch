"""Orchestration of experiments."""

DATA_LOADING_KEY = "data_loading"
REPOSITORY_ROOT_LEVEL = 3

from pathlib import Path

from orchestration.cli import parse_orchestration_arguments
from utils.path_utils import resolve_ancestor_directory
from utils.yaml_io import read_yaml


def orchestrate_experiment() -> None:
    """Orchestrate experiments."""
    args = parse_orchestration_arguments()

    ancestor_path = resolve_ancestor_directory(
        caller_file = Path(__file__),
        parent_levels=REPOSITORY_ROOT_LEVEL
    )

    print(ancestor_path)

    config_dict = read_yaml(
        file_path = ancestor_path / args.config,
    )
    print(config_dict)


if __name__ == "__main__":
    orchestrate_experiment()
