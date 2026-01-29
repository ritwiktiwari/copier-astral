# Copier-Astral

My opinionated [Copier](https://copier.readthedocs.io/) template for bootstrapping Python projects. Batteries included: linting, testing, CI/CD, docs, and containerization — all pre-configured and ready to go.

Built for my own workflow, but you're welcome to use it!

| Tool | Purpose | Benefit |
|------|---------|---------|
| **[uv](https://docs.astral.sh/uv/)** | Package management, venv, dependencies | 10-100x faster than pip |
| **[ty](https://docs.astral.sh/ty/)** | Type checking | Astral's new fast type checker |
| **[ruff](https://docs.astral.sh/ruff/)** | Linting + formatting | Replaces flake8, black, isort |
| **[pytest](https://pytest.org/)** | Testing | Industry standard |
| **[hatch](https://hatch.pypa.io/)** | Multi-version testing | Matrix testing with envs |
| **[MkDocs](https://www.mkdocs.org/)** | Documentation | Material theme + mkdocstrings |
| **[pre-commit](https://pre-commit.com/)** | Git hooks | Code quality enforcement |
| **[Typer](https://typer.tiangolo.com/)** | CLI framework | Type-hint based, modern |
| **[git-cliff](https://git-cliff.org/)** | Changelog | Auto-generated from conventional commits |

## Quick Start

### Prerequisites

- Python 3.10+
- [Copier](https://copier.readthedocs.io/) (`pip install copier`)
- [copier-template-extensions](https://github.com/copier-org/copier-template-extensions) (`pip install copier-template-extensions`)

### Generate a Project

```bash
copier copy --trust gh:YOUR_USERNAME/copier-astral my-project
```

Or from a local clone:

```bash
copier copy --trust /path/to/copier-astral my-project
```

> **Note:** The `--trust` flag is required because this template uses custom Jinja2 extensions for features like auto-detecting git user info and generating slugified package names. These extensions are safe to use but Copier warns about them by default.

### Interactive Prompts

The template will ask you about:

- **Project name** and description
- **Author information** (auto-detected from git config)
- **GitHub username** for repository URLs
- **Python version** (3.10, 3.11, 3.12, or 3.13)
- **Optional features**:
  - CLI with Typer
  - GitHub Actions CI/CD
  - Docker support
  - MkDocs documentation
  - Pre-commit hooks
  - Codecov integration
  - PyPI publishing
- **License** (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, ISC, Proprietary)

## Generated Project Structure

```
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── py.typed
│       └── cli.py           # If CLI enabled
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_my_project.py
├── docs/                     # If docs enabled
│   ├── index.md
│   ├── api.md
│   └── contributing.md
├── .github/
│   └── workflows/           # If GitHub Actions enabled
│       ├── ci.yml
│       ├── release.yml
│       └── docs.yml
├── pyproject.toml           # Single source of truth
├── hatch.toml               # Matrix testing config
├── mkdocs.yml               # If docs enabled
├── cliff.toml               # Changelog config
├── .pre-commit-config.yaml  # If pre-commit enabled
├── Dockerfile               # If Docker enabled
├── .dockerignore            # If Docker enabled
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

## Using the Generated Project

### Initial Setup

```bash
cd my-project
uv sync --all-groups
```

### Development Commands

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Type check
uv run ty check

# Build documentation
uv run mkdocs serve

# Install pre-commit hooks
pre-commit install
```

### Matrix Testing with Hatch

```bash
# Run tests across all Python versions
hatch run test:run

# Run tests with coverage across all versions
hatch run test:run-cov
```

### CLI (if enabled)

```bash
# Show help
my-project --help

# Show version
my-project --version

# Run hello command
my-project hello World
```

### Building and Publishing

```bash
# Build package
uv build

# Publish to PyPI (if configured)
uv publish
```

## GitHub Actions Workflows

- **CI** (`ci.yml`): Runs on every push/PR
  - Linting with Ruff
  - Type checking with ty
  - Tests across Python matrix
  - Coverage upload to Codecov

- **Release** (`release.yml`): Triggers on version tags
  - Builds distribution
  - Publishes to PyPI
  - Creates GitHub release with changelog

- **Docs** (`docs.yml`): Deploys to GitHub Pages
  > **Important:** If you enabled docs during setup, you must manually enable GitHub Pages in your repository. Go to **Settings → Pages → Source** and select **GitHub Actions**. Without this, the docs workflow will fail.

## Updating Projects

Copier supports updating projects to newer template versions:

```bash
cd my-project
copier update --trust
```

## Configuration

All tool configurations are centralized in `pyproject.toml`:

- Build system (hatchling)
- Dependencies
- Ruff (linting + formatting)
- ty (type checking)
- pytest
- coverage

## License

This template is released under the MIT License.
