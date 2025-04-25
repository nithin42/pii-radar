# Contributing to pii-radar

Thank you for your interest in contributing! 🎉

## Getting Started

1. **Fork** the repo and clone your fork
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Install dev dependencies: `make install`
4. Make your changes with tests
5. Run the full check: `make all`
6. Push and open a Pull Request

## Development Setup

```bash
git clone https://github.com/nithin42/pii-radar.git
cd pii-radar
pip install -e ".[dev]"
pre-commit install
```

## Running Tests

```bash
make test          # Run tests with coverage
make lint          # Lint with flake8
make format        # Format with black
make typecheck     # Type check with mypy
```

## Pull Request Guidelines

- Reference the issue your PR fixes: `Closes #N`
- Keep PRs focused — one feature or fix per PR
- Add tests for any new functionality
- Update `CHANGELOG.md` under `[Unreleased]`
- Ensure CI passes before requesting review

## Code Style

- **black** for formatting (line length 88)
- **flake8** for linting
- **mypy** strict mode for type hints — all functions must be typed
- Docstrings on all public functions and classes

## Reporting Bugs

Open a [Bug Report issue](https://github.com/nithin42/pii-radar/issues/new?template=bug_report.md).

## Requesting Features

Open a [Feature Request issue](https://github.com/nithin42/pii-radar/issues/new?template=feature_request.md).
