# User Guide

## Getting Started with Your Generated Project

### 1. Initialize the repository and install dependencies

```bash
cd my-project
git init -b main
make install
```

### 2. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 3. Run the prek hooks

If you enabled prek, install the hooks and run them to resolve any initial formatting issues:

```bash
prek install
uv run prek run -a
```

### 4. Verify everything works

```bash
make verify
make test
```

### 5. Create your GitHub repository and push

```bash
git add .
git commit -m "init: generate project from copier-astral"
git remote add origin https://github.com/YOUR_USERNAME/my-project.git
git push -u origin main
```

!!! important
    If you enabled docs during setup, you must manually enable GitHub Pages in your repository. Go to **Settings → Pages → Source** and select **GitHub Actions**. Without this, the docs workflow will fail.

### 6. Set up external services (optional)

- **Codecov**: Add your `CODECOV_TOKEN` as a [repository secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)
- **PyPI**: Add your `PYPI_TOKEN` as a repository secret. See the [PyPI docs](https://pypi.org/help/#apitoken) for creating a token
- **Renovate**: Install the [Renovate GitHub App](https://github.com/apps/renovate) and grant it access to your repository. Renovate will open pull requests automatically when new versions of GitHub Actions or Python dependencies (via `pyproject.toml`) are available

### Setting Up Renovate

1. Go to [github.com/apps/renovate](https://github.com/apps/renovate) and click **Install**
2. Choose your GitHub account or organization
3. Under **Repository access**, select **Only select repositories** and pick your repository (or choose **All repositories** if you prefer)
4. Click **Install & Authorize**
5. Renovate will open an onboarding pull request titled `Configure Renovate` — review it and merge it to activate
6. From that point on, Renovate will automatically open PRs when new versions of your dependencies are available

!!! tip
    The `renovate.json` in your project is pre-configured to manage GitHub Actions, `pyproject.toml` dependencies, and the `uv.lock` lockfile. No further configuration is needed.

### Security Scanning

If you enabled security scanning, the CI pipeline includes:

- **Gitleaks** — scans your git history for hardcoded secrets and credentials
- **pysentry-rs** — scans Python dependencies for known vulnerabilities (`make pysentry`)
- **Semgrep** — static application security testing (SAST) for common code vulnerabilities

These run automatically on every push and pull request. The Semgrep job skips PRs created by Dependabot or Renovate to avoid permission issues.

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
| `make pysentry` | Run dependency vulnerability scanning |
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
├── .pre-commit-config.yaml  # If prek enabled
├── Dockerfile               # If Docker enabled
├── .dockerignore            # If Docker enabled
├── renovate.json            # If Renovate enabled
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
