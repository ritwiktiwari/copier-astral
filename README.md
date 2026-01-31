![Copier-Astral](docs/static/copier-astral.png)

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
| **[prek](https://prek.j178.dev/)** | Git hooks | Code quality enforcement |
| **[Typer](https://typer.tiangolo.com/)** | CLI framework | Type-hint based, modern |
| **[git-cliff](https://git-cliff.org/)** | Changelog | Auto-generated from conventional commits |

## Quick Start

### Prerequisites

- Python 3.10+
- [Copier](https://copier.readthedocs.io/) (`pip install copier`)
- [copier-template-extensions](https://github.com/copier-org/copier-template-extensions) (`pip install copier-template-extensions`)

### Generate a Project

```bash
copier copy --trust gh:ritwiktiwari/copier-astral my-project
```

Or from a local clone:

```bash
copier copy --trust /path/to/copier-astral my-project
```

> **Note:** The `--trust` flag is required because this template uses custom Jinja2 extensions for features like auto-detecting git user info and generating slugified package names. These extensions are safe to use but Copier warns about them by default.

## Documentation

For the full user guide, template options, and contributing instructions, see the [documentation site](https://ritwiktiwari.github.io/copier-astral/).

## License

This template is released under the MIT License.
