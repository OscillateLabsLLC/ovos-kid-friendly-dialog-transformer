# List all recipes
default:
    @just --list

# Install dependencies from the lockfile
install:
    uv sync

install-all:
    uv sync --all-extras

# Generate lockfile from pyproject.toml
lock:
    uv lock

# Update dependencies and regenerate lockfile
upgrade:
    uv lock --upgrade

# Run Ruff linter
lint:
    ruff check .

# Run Ruff formatter
fmt:
    ruff format .

# Run both linting and formatting
check: lint fmt

# Run tests with coverage
test:
    pytest

# Run both tests and checks
validate: check test

# Clean up Python cache and build files
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete
    find . -type f -name ".coverage" -delete
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    find . -type d -name "*.egg" -exec rm -rf {} +
    find . -type d -name ".pytest_cache" -exec rm -rf {} +
    find . -type d -name ".ruff_cache" -exec rm -rf {} +
