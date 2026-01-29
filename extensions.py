"""Custom Jinja2 extensions for the Copier template."""

import re
import subprocess
import unicodedata
from datetime import datetime

from jinja2 import Environment
from jinja2.ext import Extension


def slugify(value: str) -> str:
    """Convert a string to a slug suitable for use as a Python package name.

    Args:
        value: The string to slugify.

    Returns:
        A lowercase string with spaces and special characters replaced by hyphens.
    """
    # Normalize unicode characters
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")

    # Convert to lowercase and replace spaces/special chars with hyphens
    value = re.sub(r"[^\w\s-]", "", value.lower())
    value = re.sub(r"[-\s]+", "-", value).strip("-")

    return value


def git_config(key: str) -> str:
    """Get a value from git config.

    Args:
        key: The git config command to run (e.g., 'git config user.name').

    Returns:
        The git config value or empty string if not found.
    """
    try:
        result = subprocess.run(
            key.split(),
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return ""


def github_username(_: str = "") -> str:
    """Get the GitHub username from gh CLI.

    Args:
        _: Ignored input (allows use as filter).

    Returns:
        The GitHub username or empty string if not found.
    """
    try:
        result = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return ""


class SlugifyExtension(Extension):
    """Jinja2 extension that provides the slugify filter."""

    def __init__(self, environment: Environment) -> None:
        """Initialize the extension.

        Args:
            environment: The Jinja2 environment.
        """
        super().__init__(environment)
        environment.filters["slugify"] = slugify


class GitExtension(Extension):
    """Jinja2 extension that provides git-related filters."""

    def __init__(self, environment: Environment) -> None:
        """Initialize the extension.

        Args:
            environment: The Jinja2 environment.
        """
        super().__init__(environment)
        environment.filters["git_config"] = git_config
        environment.filters["github_username"] = github_username


def current_year(_: str = "") -> str:
    """Return the current year.

    Args:
        _: Ignored input (allows use as filter).

    Returns:
        The current year as a string.
    """
    return str(datetime.now().year)


class CurrentYearExtension(Extension):
    """Jinja2 extension that provides the current year."""

    def __init__(self, environment: Environment) -> None:
        """Initialize the extension.

        Args:
            environment: The Jinja2 environment.
        """
        super().__init__(environment)
        environment.filters["current_year"] = current_year
        environment.globals["current_year"] = datetime.now().year
