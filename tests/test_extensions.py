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
