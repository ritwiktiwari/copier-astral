# Template Options

When you run `copier copy`, you'll be prompted for the following options.

## Interactive Prompts

### Project Basics

| Prompt | Type | Default | Description |
|--------|------|---------|-------------|
| `project_name` | string | — | Human-readable project name |
| `project_description` | string | `"A Python package"` | Short project description |
| `project_slug` | string | *derived from name* | Python package name (used for imports) |

### Author Information

| Prompt | Type | Default | Description |
|--------|------|---------|-------------|
| `author_name` | string | *from git config* | Author's full name |
| `author_email` | string | *from git config* | Author's email address |
| `github_username` | string | *auto-detected* | GitHub username or organization |
| `repository_name` | string | *derived from name* | Repository name on GitHub |

### Python Version

| Prompt | Type | Default | Description |
|--------|------|---------|-------------|
| `python_version` | choice | `3.12` | Minimum Python version (`3.10`–`3.13`) |
| `python_versions_matrix` | string | `"3.10,3.11,3.12,3.13"` | Python versions for CI matrix testing |

### Features

| Prompt | Type | Default | Description |
|--------|------|---------|-------------|
| `include_cli` | bool | `true` | Include CLI with Typer |
| `include_github_actions` | bool | `true` | Include GitHub Actions CI/CD |
| `include_docker` | bool | `true` | Include Dockerfile for containerization |
| `include_docs` | bool | `true` | Include MkDocs documentation |
| `include_precommit` | bool | `true` | Include pre-commit hooks |
| `include_codecov` | bool | `true` | Include Codecov integration (requires GitHub Actions) |
| `include_pypi_publish` | bool | `true` | Include automatic PyPI publishing (requires GitHub Actions) |

### License

| Prompt | Type | Default | Description |
|--------|------|---------|-------------|
| `license` | choice | `MIT` | Project license: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, ISC, or Proprietary |