# Contributing

## Development Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/copier-astral.git
cd copier-astral
make install
```

## Running Tests

The template includes a test suite that generates a project from the template and verifies it:

```bash
make test
```

To run linting and type checks:

```bash
make verify
```

Auto-fix lint and format issues:

```bash
make fix
```

## Building the Documentation

```bash
make docs-serve
```

This serves the docs locally at `http://127.0.0.1:8000/`.

## Modifying the Template

Template files live in the `template/` directory. Copier uses [Jinja2](https://jinja.palletsprojects.com/) for templating.

Key files:

- `copier.yml` — Template prompts and configuration
- `extensions.py` — Custom Jinja2 extensions (slugify, git config, etc.)
- `template/` — The generated project skeleton

### Conditional files

Files or directories can be conditionally included using Jinja2 expressions in the filename:

```
template/{% if include_docs %}mkdocs.yml{% endif %}.jinja
template/{% if include_docker %}Dockerfile{% endif %}.jinja
```

### Testing your changes

After modifying the template, run the test suite to make sure generated projects are still valid:

```bash
make test
```

You can also generate a test project manually:

```bash
copier copy --trust . /tmp/test-project
cd /tmp/test-project
make install
make verify
make test
```
