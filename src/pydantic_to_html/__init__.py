"""
pydantic-to-html: Convert Pydantic models to HTML
"""

__version__ = "0.1.1"

from .html_renderer import model_to_html, render_html

__all__ = ["model_to_html", "render_html"]