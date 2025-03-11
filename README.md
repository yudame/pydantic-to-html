# pydantic-to-html

A Python library that automatically converts Pydantic models into structured HTML using safe and semantic defaults.

## Overview

pydantic-to-html infers an appropriate HTML structure based on the types of fields in a Pydantic model, including support for nested models, lists, and forms for user input.

## Installation

```bash
pip install pydantic-to-html
```

## Usage

```python
from pydantic import BaseModel
from pydantic_to_html import model_to_html

class User(BaseModel):
    name: str
    email: str
    age: int

user = User(name="John Doe", email="john@example.com", age=30)
html = model_to_html(user)
print(html)
```

## Features

- ✅ Automatic HTML Conversion – Converts any Pydantic model into a structured HTML representation.
- ✅ Recursive Nesting – Handles nested models and lists of models gracefully.
- ✅ Table-Based Rendering – Uses <table> elements for structured data representation.
- ✅ List Support – Renders lists as <ul> or <ol>, depending on the data type.
- ✅ Automatic Form Generation – Can generate editable forms with <input> elements.
- ✅ Type-Safe Defaults – Uses appropriate form fields based on the Pydantic field type (`str`, int, bool, datetime, etc.).
- ✅ Customizable Themes – Allows passing custom CSS classes or styles.
- ✅ HTMX Support – Optionally integrates HTMX for live updates.
- ✅ Validation & Constraints – Uses Pydantic field constraints to enforce validation on form inputs.

## API

```python
def render_html(
    model: BaseModel,
    editable: bool = False,
    theme: str | None = None,
    htmx: bool = False,
    htmx_mode: str = "full",  # "full" | "inline" | "none"
    max_depth: int | None = None,
) -> str:
    """Converts a Pydantic model into HTML (table or form)."""
```

## Type Mapping

| Pydantic Type        | Default HTML Element |
|----------------------|---------------------|
| str               | <input type="text"> |
| int               | <input type="number"> |
| float             | <input type="number" step="0.01"> |
| bool              | <input type="checkbox"> |
| datetime          | <input type="datetime-local"> |
| List[str]         | Multiple <input> inside <ul> |
| List[Model]       | Nested <table> |
| Dict[str, Any]    | Table (if structured), `<ul>` otherwise |
| Enum             | Radio buttons |
| Literal[\"A\", \"B\"] | Dropdown (`<select>`) |

## HTMX Modes

| Mode      | Behavior |
|-----------|----------|
| "none"  | Static HTML |
| "inline" | <input> updates on hx-trigger="change" |
| "full"  | Whole form auto-submits on change |

## Handling Nested Models & Lists

- Lists of Primitives (`List[str]`) → <ul> with <li> elements.
- Lists of Models (`List[Model]`) → Rendered as nested tables.
- Dictionaries (`Dict[str, Any]`) → Rendered as a key-value table if structured, or <ul> if unstructured.
- Nested Pydantic Models → Recursively rendered as nested tables, with a configurable max_depth to limit depth.

## Validation & Constraints Mapping

- Min/Max Length (`Field(min_length=3, max_length=50)`) → minlength="3" maxlength="50"
- Greater Than (`Field(gt=0)`) → min="0"
- Regex Constraints (`Field(regex="^[a-z]+$"`) → pattern="^[a-z]+$"

## Error Handling for Edge Cases

- Unsupported Types (`bytes`, `UUID`, `Callable`)
  - UUID → Rendered as str(uuid)
  - bytes → Rendered as "[binary data]"
  - Callable → Rendered as "[function]"
- Default Factories (`Field(default_factory=...)`) → Rendered appropriately with their defaults.

## Roadmap

### Phase 1: Basic Rendering
- ✅ Convert flat Pydantic models into tables.
- ✅ Support nested models using recursion.
- ✅ Support lists as <ul> elements.

### Phase 2: Editable Forms
- ✅ Render models as forms with <input> fields.
- ✅ Infer input types from field types.
- ✅ Handle lists as multiple input fields.

## License

MIT