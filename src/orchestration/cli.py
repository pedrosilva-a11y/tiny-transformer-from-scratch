"""Command-Line Arguments Definition for Experiment Orchestration."""

import argparse


def parse_orchestration_arguments() -> argparse.Namespace:
    """Collect command-line arguments for orchestration.

    Returns:
        argparse.Namespace: An object containing the parsed argument attributes.

    Raises:
        SystemError: When required arguments are missing.
    """
    parser = argparse.ArgumentParser(
        description="Repository-relative Orchestrator Runner.",
    )
    
    parser.add_argument(
        "--config",
        required=True,
        help="Repository-relative path to the YAML configuration "
             "(e.g. 'conf/experiments/example.yaml')"
    )
    
    return parser.parse_args()
