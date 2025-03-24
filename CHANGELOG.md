# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-03-24

### Added
- Support for Pydantic dataclasses alongside BaseModel
- New example demonstrating dataclass support (07_dataclass_support.py)
- Comprehensive test suite for dataclass support
- Tests for edge cases with both models and dataclasses
- Documentation updates for dataclass usage

## [0.1.1] - 2025-03-11

### Changed
- Updated package metadata with correct author information
- Fixed GitHub repository URLs
- Updated copyright information

## [0.1.0] - 2025-03-11

### Added
- Initial release of pydantic-to-html
- Core API with `render_html()` and `model_to_html()` functions
- Table-based display for model data viewing
- Form generation with `editable=True` parameter
- Support for nested models with recursion
- Support for lists and dictionaries
- HTMX integration with different modes (full, inline, none)
- Theme support with built-in light and dark themes
- Custom CSS styling options
- Depth control for nested models with `max_depth` parameter
- Validation constraints from Pydantic reflected in HTML
- Complex types support (Enum, Literal, datetime, etc.)
- Comprehensive test suite
- Detailed examples with running code
- Complete documentation