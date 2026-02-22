"""Tests for the Copier template generation."""

import subprocess
from pathlib import Path

import pytest

from tests.utils import file_contains_text, file_exists, is_valid_yaml

TEMPLATE_ROOT = Path(__file__).parent.parent


@pytest.fixture
def default_answers() -> dict:
    """Default answers for template generation."""
    return {
        "project_name": "Test Project",
        "project_description": "A test project",
        "project_slug": "test_project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "github_username": "testuser",
        "repository_name": "test-project",
        "python_version": "3.12",
        "python_versions_matrix": "3.10,3.11,3.12,3.13",
        "include_cli": True,
        "include_github_actions": True,
        "include_docker": True,
        "include_docs": True,
        "include_prek": True,
        "include_codecov": True,
        "include_pypi_publish": True,
        "license": "MIT",
    }


def run_copier(tmp_path: Path, answers: dict) -> Path:
    """Run copier with the given answers.

    Args:
        tmp_path: Temporary directory for output.
        answers: Dictionary of answers to template questions.

    Returns:
        Path to the generated project.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Build copier command with data flags
    cmd = [
        "copier",
        "copy",
        str(TEMPLATE_ROOT),
        str(output_dir),
        "--defaults",
        "--force",
        "--trust",
        "--vcs-ref=HEAD",
    ]

    for key, value in answers.items():
        if isinstance(value, bool):
            cmd.extend(["-d", f"{key}={str(value).lower()}"])
        else:
            cmd.extend(["-d", f"{key}={value}"])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        raise RuntimeError(f"Copier failed: {result.stderr}")

    return output_dir


class TestBasicGeneration:
    """Tests for basic template generation."""

    def test_generates_project(self, tmp_path: Path, default_answers: dict):
        """Test that copier generates a project successfully."""
        project = run_copier(tmp_path, default_answers)
        assert project.exists()

    def test_project_name_in_readme(self, tmp_path: Path, default_answers: dict):
        """Test that project name appears in README."""
        project = run_copier(tmp_path, default_answers)
        assert file_contains_text(project / "README.md", "Test Project")

    def test_author_in_pyproject(self, tmp_path: Path, default_answers: dict):
        """Test that author info is in pyproject.toml."""
        project = run_copier(tmp_path, default_answers)
        assert file_contains_text(project / "pyproject.toml", "Test Author")
        assert file_contains_text(project / "pyproject.toml", "test@example.com")


class TestProjectStructure:
    """Tests for generated project structure."""

    def test_core_files_exist(self, tmp_path: Path, default_answers: dict):
        """Test that core project files are generated."""
        project = run_copier(tmp_path, default_answers)

        core_files = [
            "README.md",
            "pyproject.toml",
            "LICENSE",
            "CHANGELOG.md",
            ".gitignore",
        ]

        for file in core_files:
            assert file_exists(project, file), f"Missing: {file}"

    def test_src_layout(self, tmp_path: Path, default_answers: dict):
        """Test that src layout is generated correctly."""
        project = run_copier(tmp_path, default_answers)

        assert file_exists(project, "src/test_project/__init__.py")

    def test_tests_directory(self, tmp_path: Path, default_answers: dict):
        """Test that tests directory is generated."""
        project = run_copier(tmp_path, default_answers)

        assert file_exists(project, "tests/__init__.py")
        assert file_exists(project, "tests/conftest.py")

    def test_pyproject_valid_toml(self, tmp_path: Path, default_answers: dict):
        """Test that pyproject.toml is valid."""
        project = run_copier(tmp_path, default_answers)

        # Check it's parseable (TOML, not YAML, but we can check file exists)
        pyproject = project / "pyproject.toml"
        assert pyproject.exists()
        content = pyproject.read_text()
        assert "[project]" in content


class TestOptionalFeatures:
    """Tests for optional feature generation."""

    def test_docker_included(self, tmp_path: Path, default_answers: dict):
        """Test Docker files are included when enabled."""
        project = run_copier(tmp_path, default_answers)

        assert file_exists(project, "Dockerfile")
        assert file_exists(project, ".dockerignore")

    def test_docker_excluded(self, tmp_path: Path, default_answers: dict):
        """Test Docker files are excluded when disabled."""
        answers = {**default_answers, "include_docker": False}
        project = run_copier(tmp_path, answers)

        assert not file_exists(project, "Dockerfile")
        assert not file_exists(project, ".dockerignore")

    def test_github_actions_included(self, tmp_path: Path, default_answers: dict):
        """Test GitHub Actions are included when enabled."""
        project = run_copier(tmp_path, default_answers)

        assert file_exists(project, ".github/workflows")

    def test_github_actions_excluded(self, tmp_path: Path, default_answers: dict):
        """Test GitHub Actions are excluded when disabled."""
        answers = {
            **default_answers,
            "include_github_actions": False,
            "include_codecov": False,
            "include_pypi_publish": False,
        }
        project = run_copier(tmp_path, answers)

        assert not file_exists(project, ".github")

    def test_prek_included(self, tmp_path: Path, default_answers: dict):
        """Test prek config is included when enabled."""
        project = run_copier(tmp_path, default_answers)

        prek_config = project / ".pre-commit-config.yaml"
        assert prek_config.exists()
        assert is_valid_yaml(prek_config)

    def test_prek_excluded(self, tmp_path: Path, default_answers: dict):
        """Test prek config is excluded when disabled."""
        answers = {**default_answers, "include_prek": False}
        project = run_copier(tmp_path, answers)

        assert not file_exists(project, ".pre-commit-config.yaml")

    def test_docs_included(self, tmp_path: Path, default_answers: dict):
        """Test docs are included when enabled."""
        project = run_copier(tmp_path, default_answers)

        assert file_exists(project, "mkdocs.yml")
        assert file_exists(project, "docs")

    def test_docs_excluded(self, tmp_path: Path, default_answers: dict):
        """Test docs are excluded when disabled."""
        answers = {**default_answers, "include_docs": False}
        project = run_copier(tmp_path, answers)

        assert not file_exists(project, "mkdocs.yml")

    def test_cli_included(self, tmp_path: Path, default_answers: dict):
        """Test CLI is included when enabled."""
        project = run_copier(tmp_path, default_answers)

        pyproject = project / "pyproject.toml"
        assert file_contains_text(pyproject, "[project.scripts]")
        assert file_contains_text(pyproject, "typer")


class TestLicenses:
    """Tests for license generation."""

    @pytest.mark.parametrize(
        "license_type,expected_text",
        [
            ("MIT", "MIT License"),
            ("Apache-2.0", "Apache License"),
            ("GPL-3.0", "GNU GENERAL PUBLIC LICENSE"),
            ("BSD-3-Clause", "BSD"),
            ("ISC", "ISC License"),
        ],
    )
    def test_license_content(
        self,
        tmp_path: Path,
        default_answers: dict,
        license_type: str,
        expected_text: str,
    ):
        """Test that correct license is generated."""
        answers = {**default_answers, "license": license_type}
        project = run_copier(tmp_path, answers)

        license_file = project / "LICENSE"
        assert license_file.exists()
        assert file_contains_text(license_file, expected_text)


class TestPythonVersions:
    """Tests for Python version configuration."""

    @pytest.mark.parametrize("version", ["3.10", "3.11", "3.12", "3.13"])
    def test_python_version_in_pyproject(
        self, tmp_path: Path, default_answers: dict, version: str
    ):
        """Test that Python version is set in pyproject.toml."""
        answers = {**default_answers, "python_version": version}
        project = run_copier(tmp_path, answers)

        pyproject = project / "pyproject.toml"
        assert file_contains_text(pyproject, f'requires-python = ">={version}"')


class TestGitHubURLs:
    """Tests for GitHub URL generation."""

    def test_github_username_in_pyproject_urls(
        self, tmp_path: Path, default_answers: dict
    ):
        """Test that github_username appears in pyproject.toml URLs."""
        project = run_copier(tmp_path, default_answers)
        pyproject = project / "pyproject.toml"

        # Check URLs contain the github_username
        assert file_contains_text(pyproject, "https://github.com/testuser/test-project")
        assert file_contains_text(pyproject, "https://testuser.github.io/test-project")

    def test_github_username_in_readme(self, tmp_path: Path, default_answers: dict):
        """Test that github_username appears in README URLs."""
        project = run_copier(tmp_path, default_answers)
        readme = project / "README.md"

        assert file_contains_text(readme, "https://github.com/testuser/test-project")

    def test_github_username_in_mkdocs(self, tmp_path: Path, default_answers: dict):
        """Test that github_username appears in mkdocs.yml URLs."""
        project = run_copier(tmp_path, default_answers)
        mkdocs = project / "mkdocs.yml"

        assert file_contains_text(mkdocs, "https://github.com/testuser/test-project")
        assert file_contains_text(mkdocs, "testuser/test-project")

    def test_github_username_in_docs_index(self, tmp_path: Path, default_answers: dict):
        """Test that github_username appears in docs/index.md URLs."""
        project = run_copier(tmp_path, default_answers)
        docs_index = project / "docs" / "index.md"

        assert file_contains_text(
            docs_index, "https://github.com/testuser/test-project"
        )

    def test_empty_github_username_does_not_crash(
        self, tmp_path: Path, default_answers: dict
    ):
        """Test that an empty github_username doesn't crash copier.

        Regression test for: https://github.com/ritwiktiwari/copier-astral/issues/25
        When gh CLI is not installed and git config github.user is unset,
        the default is empty. Copier validates defaults before prompting,
        so the validator must not reject empty values.
        """
        answers = {**default_answers, "github_username": ""}
        project = run_copier(tmp_path, answers)
        assert project.exists()
