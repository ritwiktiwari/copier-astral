"""Tests for the custom Jinja2 extensions."""

import subprocess
from unittest.mock import patch

from jinja2 import Environment

from extensions import (
    CurrentYearExtension,
    GitExtension,
    SlugifyExtension,
    current_year,
    git_config,
    github_username,
    slugify,
)


class TestSlugify:
    """Tests for the slugify function."""

    def test_simple_string(self):
        assert slugify("Hello World") == "hello-world"

    def test_lowercase(self):
        assert slugify("UPPERCASE") == "uppercase"

    def test_special_characters(self):
        assert slugify("Hello! World?") == "hello-world"

    def test_multiple_spaces(self):
        assert slugify("Hello    World") == "hello-world"

    def test_leading_trailing_spaces(self):
        assert slugify("  Hello World  ") == "hello-world"

    def test_unicode_characters(self):
        assert slugify("Héllo Wörld") == "hello-world"

    def test_hyphens(self):
        assert slugify("hello-world") == "hello-world"

    def test_multiple_hyphens(self):
        assert slugify("hello---world") == "hello-world"

    def test_numbers(self):
        assert slugify("hello 123 world") == "hello-123-world"

    def test_empty_string(self):
        assert slugify("") == ""

    def test_only_special_characters(self):
        assert slugify("!@#$%^&*()") == ""


class TestGitConfig:
    """Tests for the git_config function."""

    def test_valid_git_config(self):
        with patch("extensions.subprocess.run") as mock_run:
            mock_run.return_value.stdout = "test-value\n"
            result = git_config("git config user.name")
            assert result == "test-value"
            mock_run.assert_called_once()

    def test_git_config_not_found(self):
        with patch("extensions.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            result = git_config("git config user.name")
            assert result == ""

    def test_git_config_subprocess_error(self):
        with patch("extensions.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.SubprocessError()
            result = git_config("git config user.name")
            assert result == ""


class TestSlugifyExtension:
    """Tests for the SlugifyExtension class."""

    def test_extension_registers_filter(self):
        env = Environment(extensions=[SlugifyExtension])
        assert "slugify" in env.filters

    def test_filter_works_in_template(self):
        env = Environment(extensions=[SlugifyExtension])
        template = env.from_string("{{ name | slugify }}")
        result = template.render(name="Hello World")
        assert result == "hello-world"


class TestGitExtension:
    """Tests for the GitExtension class."""

    def test_extension_registers_filter(self):
        env = Environment(extensions=[GitExtension])
        assert "git_config" in env.filters

    def test_filter_works_in_template(self):
        with patch("extensions.subprocess.run") as mock_run:
            mock_run.return_value.stdout = "Test User\n"
            env = Environment(extensions=[GitExtension])
            template = env.from_string("{{ cmd | git_config }}")
            result = template.render(cmd="git config user.name")
            assert result == "Test User"


class TestGitHubUsername:
    """Tests for the github_username function."""

    def test_gh_cli_success(self):
        """Test that gh CLI result is returned when available."""
        mock_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="ghuser\n", stderr=""
        )
        with patch("extensions.subprocess.run", return_value=mock_result):
            assert github_username() == "ghuser"

    def test_falls_back_to_git_config(self):
        """Test fallback to git config github.user when gh CLI fails."""
        gh_result = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr=""
        )
        git_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="gituser\n", stderr=""
        )
        with patch("extensions.subprocess.run", side_effect=[gh_result, git_result]):
            assert github_username() == "gituser"

    def test_returns_empty_when_both_fail(self):
        """Test that empty string is returned when both sources fail."""
        failed_result = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr=""
        )
        with patch("extensions.subprocess.run", return_value=failed_result):
            assert github_username() == ""

    def test_gh_cli_not_installed(self):
        """Test fallback when gh CLI is not installed."""
        git_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="gituser\n", stderr=""
        )
        with patch(
            "extensions.subprocess.run",
            side_effect=[FileNotFoundError(), git_result],
        ):
            assert github_username() == "gituser"

    def test_both_not_installed(self):
        """Test that empty string is returned when neither tool is installed."""
        with patch("extensions.subprocess.run", side_effect=FileNotFoundError()):
            assert github_username() == ""

    def test_ignores_input_parameter(self):
        """Test that the input parameter is ignored (filter compatibility)."""
        mock_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="ghuser\n", stderr=""
        )
        with patch("extensions.subprocess.run", return_value=mock_result):
            assert github_username("ignored") == "ghuser"

    def test_gh_cli_empty_stdout_triggers_fallback(self):
        """Test that empty gh CLI output triggers git config fallback."""
        gh_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        git_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="gituser\n", stderr=""
        )
        with patch("extensions.subprocess.run", side_effect=[gh_result, git_result]):
            assert github_username() == "gituser"


class TestCurrentYear:
    """Tests for the current_year function."""

    def test_returns_current_year(self):
        from datetime import datetime

        result = current_year()
        assert result == str(datetime.now().year)

    def test_ignores_input(self):
        from datetime import datetime

        result = current_year("ignored")
        assert result == str(datetime.now().year)


class TestCurrentYearExtension:
    """Tests for the CurrentYearExtension class."""

    def test_extension_registers_filter(self):
        env = Environment(extensions=[CurrentYearExtension])
        assert "current_year" in env.filters

    def test_extension_registers_global(self):
        env = Environment(extensions=[CurrentYearExtension])
        assert "current_year" in env.globals

    def test_filter_works_in_template(self):
        from datetime import datetime

        env = Environment(extensions=[CurrentYearExtension])
        template = env.from_string("{{ '' | current_year }}")
        result = template.render()
        assert result == str(datetime.now().year)

    def test_global_works_in_template(self):
        from datetime import datetime

        env = Environment(extensions=[CurrentYearExtension])
        template = env.from_string("{{ current_year }}")
        result = template.render()
        assert result == str(datetime.now().year)
