# CLAUDE.md for pydantic-to-html

## Commands
- Run all tests: `python -m unittest discover`
- Run a single test: `python -m unittest tests.test_html_renderer.TestHtmlRenderer.test_simple_model`
- Build package: `python -m build`
- Lint: `ruff check .`
- Type check: `mypy src/`
- Publish to PyPI: `./publish.sh` (uses API token from `.env` file)

## Code Style
- Use `render_html` as the primary API function (preferred over `model_to_html`)
- Docstrings: Google style with type annotations

## Documentation-Tests-Examples Alignment

The golden rule of this project is: **documentation, tests, and examples must always be in sync**.

- Every new feature needs both tests and a corresponding example in `docs/examples/`
- Examples are executable Python files with expected output in comments, doubling as informal tests/teaching tools
- When changing the API, update documentation, tests AND examples simultaneously
- Index new examples in `docs/index.md` when they're added

## Version and Release Management

Version numbers must be updated in `src/pydantic_to_html/__init__.py`, `CHANGELOG.md`, and a git tag together. See `MAINTENANCE.md` for the full release process (branching, PR flow, PyPI publish, tagging).
