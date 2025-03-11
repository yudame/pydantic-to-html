# Maintenance and Deployment Guide for pydantic-to-html

## Version Control and Release Strategy

### Branching Strategy
- `main` - Stable production code
- `develop` - Integration branch for features
- `feature/*` - Individual feature branches
- `bugfix/*` - Bug fix branches
- `release/*` - Release preparation branches

### Version Numbering
Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backward-compatible functionality
- **PATCH** version for backward-compatible bug fixes

## Development Workflow

1. **Feature Planning**
   - Create issues for features/bugs in GitHub
   - Prioritize issues in GitHub projects board
   - Document API changes in the issue

2. **Development Process**
   - Create feature branch from `develop`
   - Write tests first to define expected behavior
   - Implement the feature with full type annotations
   - Ensure all tests pass

3. **Code Quality**
   - Run linters before committing: `ruff check .`
   - Run type checking: `mypy src/`
   - Maintain test coverage >80%
   - Follow code style in CLAUDE.md

4. **Pull Request Process**
   - Submit PR from feature branch to `develop`
   - Include test cases that verify the changes
   - Add/update documentation
   - Have at least one reviewer approve

## Release Process

1. **Prepare Release**
   - Create release branch from `develop`
   - Update version in `src/pydantic_to_html/__init__.py`
   - Update CHANGELOG.md with new features and fixes
   - Final QA and documentation review

2. **Testing**
   - Run full test suite: `python -m unittest discover`
   - Verify examples work: `python examples/basic_example.py`
   - Check packaging: `python -m build --wheel`

3. **Merge and Tag**
   - Merge release branch into `main` and `develop`
   - Create version tag: `git tag -a v0.1.0 -m "First release"`
   - Push tags: `git push --tags`

4. **Publishing to PyPI**
   ```bash
   # Clean old builds
   rm -rf dist/ build/ *.egg-info/
   
   # Build distribution packages
   python -m build
   
   # Upload to PyPI
   python -m twine upload dist/*
   
   # Confirm successful upload
   pip install --upgrade pydantic-to-html
   ```

## Documentation Maintenance

- Keep README.md up-to-date with latest features
- Maintain example code in `examples/` directory
- Update API docs when interfaces change
- Consider adding auto-generated API docs with Sphinx

## Long-term Maintenance

- Review dependencies quarterly for updates
- Test compatibility with new Pydantic versions
- Monitor GitHub issues weekly
- Plan feature roadmap in 3-month cycles
- Deprecate features with warnings before removal

## Compatibility Strategy

- Support the latest two Python versions
- Always test against the latest Pydantic version
- Maintain backward compatibility for at least one year
- Clearly document breaking changes in CHANGELOG.md