# CLAUDE.md for pydantic-to-html

## Commands
- Run all tests: `python -m unittest discover`
- Run a single test: `python -m unittest tests.test_html_renderer.TestHtmlRenderer.test_simple_model`
- Build package: `python -m build`
- Lint: `ruff check .`
- Type check: `mypy src/`
- Publish to PyPI: `twine upload dist/*`

## Code Style
- Use Python 3.11+ features and type hints everywhere
- Imports: standard library first, then third-party, then local
- Classes use PascalCase, functions/variables use snake_case
- Private functions/variables prefixed with underscore
- Line length: 88 characters (Black compatible)
- Docstrings using Google style with type annotations
- Error handling: use explicit exception types, prefer early returns
- Keep code modular and focused on HTML generation with pure functions
- Follow Pydantic v2 patterns and conventions
- Use `render_html` as the primary API function (preferred over `model_to_html`)

## Development Process
1. Gather requirements and clearly define functionality
2. Write tests that define expected behavior
3. Implement features until tests pass
4. Commit changes with descriptive messages
5. Review code for potential improvements
6. Refactor code while ensuring tests continue to pass
7. Final commit and publish to PyPI

## Publishing Workflow
```bash
# Install build tools if needed
pip install build twine

# Run tests to ensure quality
python -m unittest discover

# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```