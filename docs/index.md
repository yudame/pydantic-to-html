# pydantic-to-html

A Python library for converting Pydantic models to HTML.

## Overview

`pydantic-to-html` provides a simple way to convert Pydantic models to HTML, with support for nested models, forms, and various styling options.

## Installation

```bash
pip install pydantic-to-html
```

## Basic Usage

```python
from pydantic import BaseModel
from pydantic_to_html import render_html

class Person(BaseModel):
    name: str
    age: int
    is_active: bool

person = Person(name="John Doe", age=30, is_active=True)
html = render_html(person)
```

## Examples

The examples directory contains a variety of examples showing different usage scenarios:

1. [Basic Usage](examples/01_basic_usage.py) - Simple model rendering
2. [Nested Models](examples/02_nested_models.py) - Working with complex nested structures
3. [Editable Forms](examples/03_editable_forms.py) - Generate editable HTML forms
4. [Themes and Styling](examples/04_themes_and_styling.py) - Customize the appearance
5. [HTMX Integration](examples/05_htmx_integration.py) - Add interactive elements
6. [Depth Control](examples/06_depth_control.py) - Limit rendering depth for complex models
7. [Dataclass Support](examples/07_dataclass_support.py) - Using both Pydantic models and dataclasses

## API Reference

### `render_html()`

```python
def render_html(
    model: Any,  # BaseModel or dataclass
    editable: bool = False,
    theme: str | None = None,
    htmx: bool = False,
    htmx_mode: str = "full",  # "full" | "inline" | "none"
    max_depth: int | None = None,
) -> str:
    """Converts a Pydantic model or dataclass into HTML (table or form)."""
```

**Parameters:**
- `model` - The Pydantic model or dataclass to convert
- `editable` - Whether to render as an editable form
- `theme` - Optional theme name (e.g., "light", "dark")
- `htmx` - Whether to include HTMX attributes
- `htmx_mode` - The HTMX update mode
- `max_depth` - Maximum depth for nested models

### `model_to_html()`

Legacy API, maintained for backward compatibility:

```python
def model_to_html(
    model: Any,  # BaseModel or dataclass
    include_css: bool = True,
    custom_css: str | None = None,
) -> str:
    """Convert a Pydantic model or dataclass to HTML."""
```

## Contributing

Contributions are welcome! Please see the [MAINTENANCE.md](MAINTENANCE.md) file for guidelines.