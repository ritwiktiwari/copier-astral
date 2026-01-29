.PHONY: verify fix lint format type-check install test

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
	uv sync --group dev

# Run tests
test:
	uv run pytest tests/ -v
