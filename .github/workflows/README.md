# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automated testing and publishing.

## Workflow: Publish to PyPI

File: `workflow.yml`

This workflow handles testing and publishing the package to PyPI. It runs in two scenarios:

1. **When a GitHub release is published**
   - Automatically runs tests and publishes to PyPI
   - No manual input required

2. **Manually via workflow_dispatch**
   - Can be triggered manually from the Actions tab
   - Allows selecting the version bump type (patch, minor, major)

### Setting up PyPI Publishing

To enable publishing to PyPI, you need to:

1. Create a `pypi` environment in your GitHub repository:
   - Go to repository Settings -> Environments
   - Create a new environment named `pypi`
   - Add environment protection rules if desired

2. Add the following secrets to the `pypi` environment:
   - `PYPI_USERNAME`: Your PyPI username (or `__token__` if using API token)
   - `PYPI_API_TOKEN`: Your PyPI API token

### Workflow Structure

The workflow has two jobs:

1. **test**: Runs the test suite on multiple Python versions
   - Installs dependencies
   - Runs pytest with coverage
   - Performs type checking with mypy
   - Runs linting with ruff

2. **build-and-publish**: Builds and publishes the package
   - Only runs if tests pass
   - Builds the package using build
   - Publishes to PyPI using twine
   - Verifies the upload by installing the package