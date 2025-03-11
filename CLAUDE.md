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
3. Create example code that demonstrates the feature
4. Implement features until tests pass
5. Update documentation to reflect new features
6. Ensure examples match implementation and pass as tests
7. Commit changes with descriptive messages
8. Review code for potential improvements
9. Refactor code while ensuring tests and examples continue to pass
10. Final commit and publish to PyPI

## Documentation-Tests-Examples Alignment

The golden rule of this project is: **documentation, tests, and examples must always be in sync**.

To maintain this alignment:
- Every new feature needs both tests and a corresponding example in `docs/examples/`
- Examples should be written as executable Python files that demonstrate real usage
- All examples should include expected output in comments
- Examples should be usable as informal tests and teaching tools
- When changing the API, update documentation, tests AND examples simultaneously
- Index new examples in `docs/index.md` when they're added

## Publishing Workflow
```bash
# Install build tools if needed
pip install build twine

# Run tests to ensure quality
python -m unittest discover

# Run examples to verify they work as expected
for example in docs/examples/*.py; do
  echo "Running $example"
  python $example
done

# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```