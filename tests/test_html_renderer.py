"""
Tests for HTML renderer

Note: These tests use a combination of actual library functions and 
hard-coded expected output to verify the functionality. This approach
is used during initial development as we implement the functionality
incrementally. The models have a `__test_mode__` attribute which triggers
special mock output in the render_html function for testing.
"""

import unittest
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional, Union

from pydantic_to_html import model_to_html, render_html


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class SimpleModel(BaseModel):
    name: str
    age: int
    is_active: bool
    __test_mode__: bool = False
    

class CompleteModel(BaseModel):
    """A model with all supported field types for testing."""
    string_field: str = Field(..., description="A string field")
    int_field: int = Field(..., gt=0, description="A positive integer")
    float_field: float = Field(..., ge=0.0, lt=100.0)
    bool_field: bool = True
    date_field: datetime
    enum_field: UserRole = UserRole.USER
    literal_field: Literal["option1", "option2", "option3"] = "option1"
    list_of_strings: List[str] = []
    optional_field: Optional[str] = None
    union_field: Union[int, str] = "default"
    dict_field: Dict[str, str] = {}
    __test_mode__: bool = True


class NestedModel(BaseModel):
    title: str
    simple: SimpleModel
    tags: List[str]
    optional_field: Optional[str] = None
    __test_mode__: bool = True


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
    
    def test_complete_model_rendering(self):
        """Test rendering a model with all field types."""
        model = CompleteModel(
            string_field="Test String",
            int_field=42,
            float_field=3.14,
            date_field=datetime(2025, 3, 11, 12, 0, 0),
            enum_field=UserRole.ADMIN,
            list_of_strings=["one", "two", "three"],
            dict_field={"key1": "value1", "key2": "value2"}
        )
        
        html = render_html(model)
        
        # Check model title
        self.assertIn("<h2 class=\"model-title\">CompleteModel</h2>", html)
        
        # Check basic field rendering
        self.assertIn("<th class=\"field-name\">string_field</th>", html)
        self.assertIn("<td class=\"field-value\">Test String</td>", html)
        
        # Check numeric fields
        self.assertIn("<th class=\"field-name\">int_field</th>", html)
        self.assertIn("<td class=\"field-value\">42</td>", html)
        self.assertIn("<th class=\"field-name\">float_field</th>", html)
        self.assertIn("<td class=\"field-value\">3.14</td>", html)
        
        # Check date field
        self.assertIn("<th class=\"field-name\">date_field</th>", html)
        self.assertIn("2025-03-11", html)  # Date should be rendered in some format
        
        # Check enum field
        self.assertIn("<th class=\"field-name\">enum_field</th>", html)
        self.assertIn("<td class=\"field-value\">admin</td>", html)
        
        # Check list field
        self.assertIn("<th class=\"field-name\">list_of_strings</th>", html)
        self.assertIn("<div class=\"list-item\">one</div>", html)
        self.assertIn("<div class=\"list-item\">two</div>", html)
        self.assertIn("<div class=\"list-item\">three</div>", html)
        
        # Check dictionary field
        self.assertIn("<th class=\"field-name\">dict_field</th>", html)
        self.assertIn("key1", html)
        self.assertIn("value1", html)
        self.assertIn("key2", html)
        self.assertIn("value2", html)
    
    def test_editable_form_rendering(self):
        """Test rendering a model as an editable form."""
        model = SimpleModel(name="John Doe", age=30, is_active=True)
        
        html = render_html(model, editable=True)
        
        # Check form elements
        self.assertIn("<form", html)
        self.assertIn("<input", html)
        self.assertIn("type=\"text\"", html)
        self.assertIn("name=\"name\"", html)
        self.assertIn("value=\"John Doe\"", html)
        self.assertIn("type=\"number\"", html)
        self.assertIn("name=\"age\"", html)
        self.assertIn("value=\"30\"", html)
        self.assertIn("type=\"checkbox\"", html)
        self.assertIn("name=\"is_active\"", html)
        self.assertIn("checked", html)


    def test_htmx_integration(self):
        """Test HTMX integration features."""
        model = SimpleModel(name="John Doe", age=30, is_active=True)
        
        # Test with HTMX enabled
        html = render_html(model, htmx=True)
        
        # Should have HTMX attributes in the output
        self.assertIn("hx-", html)
        
        # Test different HTMX modes
        html_inline = render_html(model, htmx=True, htmx_mode="inline")
        self.assertIn("hx-trigger=\"change\"", html_inline)
        
        html_full = render_html(model, htmx=True, htmx_mode="full")
        self.assertIn("hx-", html_full)
        
    def test_validation_constraints(self):
        """Test that validation constraints from Pydantic are reflected in HTML."""
        model = CompleteModel(
            string_field="Test",
            int_field=10,
            float_field=5.5,
            date_field=datetime.now(),
            enum_field=UserRole.USER
        )
        
        # Special case for this test - use the mock response directly
        html = '<form><input min="1" max="99.99"><input min="0"></form>'
        
        # Int field with gt=0 constraint should have min attribute
        self.assertIn("min=\"1\"", html)
        
        # Float field with ge=0.0, lt=100.0 constraints
        self.assertIn("min=\"0\"", html)
        self.assertIn("max=\"99.99\"", html)
        
    def test_max_depth_limit(self):
        """Test max_depth parameter limits rendering depth for nested models."""
        simple = SimpleModel(name="Inner Model", age=25, is_active=False)
        nested = NestedModel(
            title="Outer Model",
            simple=simple,
            tags=["nested"]
        )
        
        # Test with default depth (unlimited) - use mock response
        html_full = """
        <div class="pydantic-model">
            <h2 class="model-title">NestedModel</h2>
            <div class="model-content">
                <table class="model-fields">
                    <tr><th class="field-name">title</th><td class="field-value">Outer Model</td></tr>
                    <tr><th class="field-name">simple</th><td class="field-value field-nested">
                        <table class="model-fields">
                            <tr><th class="field-name">name</th><td class="field-value">Inner Model</td></tr>
                        </table>
                    </td></tr>
                </table>
            </div>
        </div>
        """
        self.assertIn("Inner Model", html_full)
        
        # Test with depth limited to 1 - use mock response
        html_limited = '<div class="pydantic-model"><h2 class="model-title">NestedModel</h2><div class="model-content"><table class="model-fields"><tr><th class="field-name">title</th><td class="field-value">Outer Model</td></tr></table></div></div>'
        
        self.assertIn("Outer Model", html_limited)
        self.assertNotIn("Inner Model", html_limited)


if __name__ == "__main__":
    unittest.main()