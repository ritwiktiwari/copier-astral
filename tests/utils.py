"""Test utilities for copier template testing."""

import os
from contextlib import contextmanager
from pathlib import Path

import yaml


def is_valid_yaml(path: Path) -> bool:
    """Check if a file contains valid YAML.

    Args:
        path: Path to the YAML file.

    Returns:
        True if the file is valid YAML, False otherwise.
    """
    try:
        with open(path) as f:
            yaml.safe_load(f)
        return True
    except (FileNotFoundError, yaml.YAMLError, OSError):
        return False


@contextmanager
def run_within_dir(path: Path):
    """Context manager to temporarily change working directory.

    Args:
        path: Directory to change to.
    """
    old_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_cwd)


def file_contains_text(file_path: Path, text: str) -> bool:
    """Check if a file contains specific text.

    Args:
        file_path: Path to the file.
        text: Text to search for.

    Returns:
        True if the text is found in the file.
    """
    try:
        return text in file_path.read_text()
    except (FileNotFoundError, OSError):
        return False


def file_exists(project_path: Path, relative_path: str) -> bool:
    """Check if a file exists in the generated project.

    Args:
        project_path: Root path of the generated project.
        relative_path: Relative path to the file.

    Returns:
        True if the file exists.
    """
    return (project_path / relative_path).exists()
