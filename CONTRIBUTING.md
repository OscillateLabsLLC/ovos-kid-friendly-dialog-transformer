# Contributing to ovos-kid-friendly-dialog-transformer

Thanks for your interest in contributing!

**Note:** This project is a **Proof of Concept**. It is experimental and not recommended for production use. Contributions are welcome but the project may not be actively maintained.

## Development Setup

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager
- [just](https://github.com/casey/just) task runner (optional but recommended)
- [Ollama](https://ollama.com) running locally for integration testing

### Getting Started

```bash
git clone https://github.com/OscillateLabsLLC/ovos-kid-friendly-dialog-transformer
cd ovos-kid-friendly-dialog-transformer

# Install dependencies
just install
# or
uv sync
```

## Common Commands

```bash
# Install dependencies
just install

# Run tests
just test

# Run linter
just lint

# Format code
just fmt

# Run linting and formatting
just check

# Run all checks and tests
just validate

# Clean build artifacts
just clean

# Show all available commands
just --list
```

Or directly with uv:

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

## Pull Requests

1. Create a feature branch: `git checkout -b feat/my-change`
2. Make your changes
3. Run `just validate` to ensure tests and linting pass
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
5. Open a pull request

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.
