.PHONY: verify fix lint format type-check install test docs docs-serve

# Verify - check everything without making changes
verify: lint format-check type-check

# Fix - automatically fix what can be fixed
fix:
	uvx ruff check --fix .
	uvx ruff format .

# Individual targets
lint:
	uvx ruff check .

format-check:
	uvx ruff format --check .

format:
	uvx ruff format .

type-check:
	uvx ty check

# Install dependencies
install:
	uv sync --all-groups

# Run tests
test:
	uv run pytest tests/ -v

# Documentation
docs:
	uv run --group docs mkdocs build

docs-serve:
	uv run --group docs mkdocs serve

# Secret scanning
secrets:
	gitleaks detect --redact 80 --no-banner --timeout 2 --max-target-megabytes=2 -v

# Dependency audit
pysentry:
	uv run pysentry-rs
