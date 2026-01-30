![Copier-Astral](static/copier-astral.png)

---

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

## Getting Started with Your Generated Project

### 1. Initialize the repository and install dependencies

```bash
cd my-project
git init -b main
make install
```

### 2. Run the pre-commit hooks

If you enabled pre-commit, install the hooks and run them to resolve any initial formatting issues:

```bash
pre-commit install
uv run pre-commit run -a
```

### 3. Verify everything works

```bash
make verify
make test
```

### 4. Create your GitHub repository and push

```bash
git add .
git commit -m "init: generate project from copier-astral"
git remote add origin git@github.com:YOUR_USERNAME/my-project.git
git push -u origin main
```

> **Important:** If you enabled docs during setup, you must manually enable GitHub Pages in your repository. Go to **Settings → Pages → Source** and select **GitHub Actions**. Without this, the docs workflow will fail.

### 5. Set up external services (optional)

- **Codecov**: Add your `CODECOV_TOKEN` as a [repository secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)
- **PyPI**: Add your `PYPI_TOKEN` as a repository secret. See the [PyPI docs](https://pypi.org/help/#apitoken) for creating a token

## Development Commands

All commands are available via `make`:

| Command | Description |
|---------|-------------|
| `make install` | Install all dependencies |
| `make verify` | Run all checks (lint, format, type-check) |
| `make fix` | Auto-fix lint and format issues |
| `make test` | Run tests |
| `make test-cov` | Run tests with coverage |
| `make test-matrix` | Run tests across all Python versions |
| `make test-matrix-cov` | Run tests with coverage across all versions |
| `make docs` | Build documentation |
| `make docs-serve` | Serve documentation locally |

## Releasing a New Version

1. Create a new version tag:

   ```bash
   git tag v0.1.0
   git push --tags
   ```

2. The `release.yml` workflow will automatically:
   - Build the distribution
   - Publish to PyPI (if configured)
   - Create a GitHub release with changelog

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
├── Makefile                 # Development commands
├── pyproject.toml           # Single source of truth
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

## Updating Existing Projects

Copier supports updating projects to newer template versions:

```bash
cd my-project
copier update --trust
```

## License

This template is released under the MIT License.
