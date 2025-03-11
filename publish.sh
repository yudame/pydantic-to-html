#!/bin/bash
# Script to publish pydantic-to-html to PyPI

# Ensure we're in the right directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check for .env file
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create one based on .env.example"
    exit 1
fi

# Load environment variables from .env
source .env

# Check for API token format
if [ "$pypi_username" != "__token__" ]; then
    echo "Error: PyPI now requires API token authentication."
    echo "Please update your .env file with:"
    echo "pypi_username=__token__"
    echo "pypi_password=pypi-your-token-here"
    exit 1
fi

# Clean previous builds
rm -rf dist/ build/ *.egg-info/ 2>/dev/null

# Detect Python command
if command -v python3 &>/dev/null; then
    PYTHON=python3
    PIP=pip3
elif command -v python &>/dev/null; then
    PYTHON=python
    PIP=pip
else
    echo "Error: Python not found. Please install Python 3."
    exit 1
fi

# Run tests
echo "Running tests..."
$PYTHON -m unittest discover
if [ $? -ne 0 ]; then
    echo "Error: Tests failed. Aborting publish."
    exit 1
fi

# Build package
echo "Building package..."
$PYTHON -m build
if [ $? -ne 0 ]; then
    echo "Error: Build failed. Aborting publish."
    exit 1
fi

# Upload to PyPI
echo "Uploading to PyPI..."
TWINE_USERNAME=$pypi_username TWINE_PASSWORD=$pypi_password $PYTHON -m twine upload dist/*

# Verify the upload
echo "Verifying upload..."
$PIP install --upgrade pydantic-to-html

echo "Publish process complete!"