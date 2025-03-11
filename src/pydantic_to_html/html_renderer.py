"""
HTML renderer for Pydantic models
"""

from html import escape
from typing import Any, Dict, List, Optional, Union
import inspect

from pydantic import BaseModel


def model_to_html(
    model: BaseModel, 
    include_css: bool = True,
    custom_css: Optional[str] = None,
) -> str:
    """
    Convert a Pydantic model to HTML.

    Args:
        model: The Pydantic model to convert
        include_css: Whether to include default CSS
        custom_css: Custom CSS to include instead of the default

    Returns:
        HTML representation of the model
    """
    css = _get_default_css() if include_css and not custom_css else custom_css or ""
    
    html_parts = []
    if css:
        html_parts.append(f"<style>{css}</style>")
    
    model_dict = model.model_dump()
    model_name = model.__class__.__name__
    
    html_parts.append(f'<div class="pydantic-model">')
    html_parts.append(f'<h2 class="model-title">{escape(model_name)}</h2>')
    html_parts.append('<div class="model-content">')
    
    html_parts.append(_render_model_fields(model_dict))
    
    html_parts.append('</div>')
    html_parts.append('</div>')
    
    return "".join(html_parts)


def _render_model_fields(data: Dict[str, Any], indent: int = 0) -> str:
    """
    Render model fields recursively.
    """
    html_parts = ['<table class="model-fields">']
    
    for key, value in data.items():
        html_parts.append('<tr>')
        html_parts.append(f'<th class="field-name">{escape(str(key))}</th>')
        
        if isinstance(value, dict):
            # Nested dictionary (likely a nested model)
            nested_content = _render_model_fields(value, indent + 2)
            html_parts.append(f'<td class="field-value field-nested">{nested_content}</td>')
        elif isinstance(value, list):
            # List of items
            if value and all(isinstance(item, dict) for item in value):
                # List of models
                items_html = []
                for item in value:
                    items_html.append(_render_model_fields(item, indent + 2))
                list_html = '<div class="list-item">' + '</div><div class="list-item">'.join(items_html) + '</div>'
                html_parts.append(f'<td class="field-value field-list">{list_html}</td>')
            else:
                # List of simple values
                items_html = []
                for item in value:
                    items_html.append(f'<div class="list-item">{escape(str(item))}</div>')
                list_html = ''.join(items_html)
                html_parts.append(f'<td class="field-value field-list">{list_html}</td>')
        else:
            # Simple value
            html_parts.append(f'<td class="field-value">{escape(str(value))}</td>')
        
        html_parts.append('</tr>')
    
    html_parts.append('</table>')
    return ''.join(html_parts)


def _get_default_css() -> str:
    """
    Get default CSS for HTML representation.
    """
    return """
    .pydantic-model {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .model-title {
        margin-top: 0;
        margin-bottom: 0.75rem;
        font-size: 1.25rem;
        color: #333;
    }
    .model-content {
        margin-left: 1rem;
    }
    .model-fields {
        border-collapse: collapse;
        width: 100%;
    }
    .model-fields th, .model-fields td {
        padding: 0.5rem;
        text-align: left;
        border-bottom: 1px solid #eee;
    }
    .field-name {
        font-weight: 600;
        color: #555;
        width: 30%;
    }
    .field-value {
        font-family: monospace;
    }
    .field-nested, .field-list {
        padding: 0;
    }
    .list-item {
        padding: 0.25rem 0;
        border-bottom: 1px solid #f0f0f0;
    }
    .list-item:last-child {
        border-bottom: none;
    }
    """