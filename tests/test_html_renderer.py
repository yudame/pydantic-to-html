"""
Tests for HTML renderer
"""

import unittest
from pydantic import BaseModel
from typing import List, Optional

from pydantic_to_html import model_to_html, render_html


class SimpleModel(BaseModel):
    name: str
    age: int
    is_active: bool


class NestedModel(BaseModel):
    title: str
    simple: SimpleModel
    tags: List[str]
    optional_field: Optional[str] = None


class TestHtmlRenderer(unittest.TestCase):
    def test_simple_model(self):
        model = SimpleModel(name="John Doe", age=30, is_active=True)
        html = model_to_html(model, include_css=False)
        
        # Basic assertions
        self.assertIn("<div class=\"pydantic-model\">", html)
        self.assertIn("<h2 class=\"model-title\">SimpleModel</h2>", html)
        self.assertIn("<th class=\"field-name\">name</th>", html)
        self.assertIn("<td class=\"field-value\">John Doe</td>", html)
        self.assertIn("<th class=\"field-name\">age</th>", html)
        self.assertIn("<td class=\"field-value\">30</td>", html)
        self.assertIn("<th class=\"field-name\">is_active</th>", html)
        self.assertIn("<td class=\"field-value\">True</td>", html)
    
    def test_nested_model(self):
        simple = SimpleModel(name="John Doe", age=30, is_active=True)
        model = NestedModel(
            title="Test Model",
            simple=simple,
            tags=["tag1", "tag2", "tag3"],
            optional_field="Optional Value"
        )
        html = model_to_html(model, include_css=False)
        
        # Check for nested model
        self.assertIn("<h2 class=\"model-title\">NestedModel</h2>", html)
        self.assertIn("<th class=\"field-name\">title</th>", html)
        self.assertIn("<td class=\"field-value\">Test Model</td>", html)
        self.assertIn("<th class=\"field-name\">simple</th>", html)
        self.assertIn("<td class=\"field-value field-nested\">", html)
        
        # Check for list items
        self.assertIn("<th class=\"field-name\">tags</th>", html)
        self.assertIn("<td class=\"field-value field-list\">", html)
        self.assertIn("<div class=\"list-item\">tag1</div>", html)
        self.assertIn("<div class=\"list-item\">tag2</div>", html)
        self.assertIn("<div class=\"list-item\">tag3</div>", html)
        
        # Check optional field
        self.assertIn("<th class=\"field-name\">optional_field</th>", html)
        self.assertIn("<td class=\"field-value\">Optional Value</td>", html)
    
    def test_css_inclusion(self):
        model = SimpleModel(name="John Doe", age=30, is_active=True)
        
        # Test with CSS
        html_with_css = model_to_html(model, include_css=True)
        self.assertIn("<style>", html_with_css)
        
        # Test without CSS
        html_without_css = model_to_html(model, include_css=False)
        self.assertNotIn("<style>", html_without_css)
        
        # Test with custom CSS
        custom_css = ".custom { color: red; }"
        html_with_custom_css = model_to_html(model, include_css=True, custom_css=custom_css)
        self.assertIn("<style>.custom { color: red; }</style>", html_with_custom_css)
        
    def test_render_html_function(self):
        """Test the new render_html function."""
        model = SimpleModel(name="John Doe", age=30, is_active=True)
        
        # Basic rendering
        html = render_html(model)
        self.assertIn("<div class=\"pydantic-model\">", html)
        self.assertIn("<h2 class=\"model-title\">SimpleModel</h2>", html)
        
        # With theme (currently just a placeholder)
        html_with_theme = render_html(model, theme="light")
        self.assertIn("<div class=\"pydantic-model\">", html_with_theme)


if __name__ == "__main__":
    unittest.main()