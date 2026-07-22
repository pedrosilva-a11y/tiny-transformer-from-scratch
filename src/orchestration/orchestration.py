"""Orchestration of experiments."""

import sys
from pathlib import Path

from pydantic import ValidationError

from data_loading.data_loading import load_data
from orchestration.cli import parse_orchestration_arguments
from orchestration.schema import ExperimentConfig
from tokenization.tokenization import build_tokens
from utils.path_utils import resolve_ancestor_directory
from utils.yaml_io import read_yaml

CONFIG_VALIDATION_EXIT_CODE = 1
REPOSITORY_ROOT_LEVEL = 3


def orchestrate_experiment() -> None:
    """Orchestrate experiments."""
    args = parse_orchestration_arguments()

    repository_root_path = resolve_ancestor_directory(
        caller_file=Path(__file__),
        parent_levels=REPOSITORY_ROOT_LEVEL,
    )

    config_dict = read_yaml(
        file_path = repository_root_path / args.config,
    )

    try:
        config = ExperimentConfig.run_validation(config=config_dict) 
    except ValidationError as e:
        print(
            f"Configuration Validation Error:\n{e}",
            file=sys.stderr,
        )
        sys.exit(CONFIG_VALIDATION_EXIT_CODE)

    
    loaded_data = load_data(data_loading_config=config.data_loading)

    print(loaded_data[:100])

    tokens_sorted = build_tokens(raw_input=loaded_data)

    print(tokens_sorted)

    print(len(tokens_sorted))


if __name__ == "__main__":
    orchestrate_experiment()
