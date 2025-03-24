"""
Tests for dataclass support
"""

import unittest
from datetime import datetime, date
from enum import Enum
from typing import List, Optional, Dict, Union, Literal

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass as pydantic_dataclass

from pydantic_to_html import render_html, model_to_html


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


# Standard Pydantic model for comparison
class Address(BaseModel):
    street: str
    city: str
    zip_code: str
    country: str = "USA"


class User(BaseModel):
    name: str
    email: str
    age: int = Field(gt=0)
    role: UserRole = UserRole.USER
    created_at: datetime
    address: Optional[Address] = None


# Pydantic dataclass version
@pydantic_dataclass
class AddressDataClass:
    street: str
    city: str
    zip_code: str
    country: str = "USA"


@pydantic_dataclass
class UserDataClass:
    name: str
    email: str
    age: int
    created_at: datetime
    role: UserRole = UserRole.USER
    address: Optional[AddressDataClass] = None


# Complex models for testing all features
class ComplexModel(BaseModel):
    string_field: str
    int_field: int = Field(gt=0, lt=100)
    float_field: float = Field(ge=0.0, le=1.0)
    date_field: date
    enum_field: UserRole
    literal_field: Literal["option1", "option2", "option3"] = "option1"
    list_of_strings: List[str]
    list_of_models: List[Address]
    dict_field: Dict[str, str]
    union_field: Union[int, str]
    nested_model: Address


@pydantic_dataclass
class ComplexDataClass:
    string_field: str
    int_field: int
    float_field: float
    date_field: date
    enum_field: UserRole
    list_of_strings: List[str]
    list_of_models: List[AddressDataClass]
    dict_field: Dict[str, str]
    union_field: Union[int, str]
    nested_model: AddressDataClass
    literal_field: Literal["option1", "option2", "option3"] = "option1"


class TestDataClassSupport(unittest.TestCase):
    def setUp(self):
        # Create basic test data
        self.address = Address(
            street="123 Main St",
            city="Anytown",
            zip_code="12345"
        )
        
        self.user = User(
            name="John Doe",
            email="john@example.com",
            age=30,
            role=UserRole.ADMIN,
            created_at=datetime(2025, 3, 24, 12, 0, 0),
            address=self.address
        )
        
        # Same data but with dataclasses
        self.address_dc = AddressDataClass(
            street="123 Main St",
            city="Anytown",
            zip_code="12345"
        )
        
        self.user_dc = UserDataClass(
            name="John Doe",
            email="john@example.com",
            age=30,
            role=UserRole.ADMIN,
            created_at=datetime(2025, 3, 24, 12, 0, 0),
            address=self.address_dc
        )
        
        # Create complex test data
        self.complex_model = ComplexModel(
            string_field="Test String",
            int_field=50,
            float_field=0.5,
            date_field=date(2025, 3, 24),
            enum_field=UserRole.USER,
            literal_field="option2",
            list_of_strings=["one", "two", "three"],
            list_of_models=[self.address, self.address],
            dict_field={"key1": "value1", "key2": "value2"},
            union_field="string value",
            nested_model=self.address
        )
        
        # Same complex data but with dataclasses
        self.complex_dc = ComplexDataClass(
            string_field="Test String",
            int_field=50,
            float_field=0.5,
            date_field=date(2025, 3, 24),
            enum_field=UserRole.USER,
            literal_field="option2",
            list_of_strings=["one", "two", "three"],
            list_of_models=[self.address_dc, self.address_dc],
            dict_field={"key1": "value1", "key2": "value2"},
            union_field="string value",
            nested_model=self.address_dc
        )
    
    def test_dataclass_basic_rendering(self):
        """Test that dataclasses can be rendered similarly to BaseModel."""
        # Render both versions
        html_model = render_html(self.user)
        html_dataclass = render_html(self.user_dc)
        
        # Basic structure checks
        self.assertIn("<h2 class=\"model-title\">UserDataClass</h2>", html_dataclass)
        self.assertIn("<th class=\"field-name\">name</th>", html_dataclass)
        self.assertIn("<td class=\"field-value\">John Doe</td>", html_dataclass)
        
        # Check for nested model rendering
        self.assertIn("<th class=\"field-name\">address</th>", html_dataclass)
        self.assertIn("<td class=\"field-value field-nested\">", html_dataclass)
        self.assertIn("123 Main St", html_dataclass)
        
        # Check for enum rendering
        self.assertIn("<th class=\"field-name\">role</th>", html_dataclass)
        self.assertIn("<td class=\"field-value\">admin</td>", html_dataclass)

    def test_dataclass_form_rendering(self):
        """Test that dataclasses can be rendered as forms."""
        html_form = render_html(self.user_dc, editable=True)
        
        # Check form elements
        self.assertIn("<form", html_form)
        self.assertIn("<input", html_form)
        self.assertIn("type=\"text\"", html_form)
        self.assertIn("name=\"name\"", html_form)
        self.assertIn("value=\"John Doe\"", html_form)
        
        # Check for age field with proper type
        self.assertIn("type=\"number\"", html_form)
        self.assertIn("name=\"age\"", html_form)
        self.assertIn("value=\"30\"", html_form)
    
    def test_legacy_api_with_dataclasses(self):
        """Test the legacy model_to_html function with dataclasses."""
        html = model_to_html(self.user_dc)
        
        # Basic checks
        self.assertIn("<h2 class=\"model-title\">UserDataClass</h2>", html)
        self.assertIn("<th class=\"field-name\">name</th>", html)
        self.assertIn("<td class=\"field-value\">John Doe</td>", html)
        
        # With CSS options
        html_with_css = model_to_html(self.user_dc, include_css=True)
        self.assertIn("<style>", html_with_css)
        
        html_no_css = model_to_html(self.user_dc, include_css=False)
        self.assertNotIn("<style>", html_no_css)
        
        custom_css = ".test{color:red;}"
        html_custom_css = model_to_html(self.user_dc, custom_css=custom_css)
        self.assertIn(custom_css, html_custom_css)
    
    def test_htmx_with_dataclasses(self):
        """Test HTMX integration with dataclasses."""
        # Standard HTMX
        html_htmx = render_html(self.user_dc, htmx=True)
        self.assertIn("hx-", html_htmx)
        
        # HTMX with inline mode
        html_inline = render_html(self.user_dc, htmx=True, htmx_mode="inline", editable=True)
        self.assertIn("hx-trigger=\"change\"", html_inline)
        
        # HTMX with full mode
        html_full = render_html(self.user_dc, htmx=True, htmx_mode="full", editable=True)
        self.assertIn("hx-post=\"/submit\"", html_full)
        
        # HTMX with none mode
        html_none = render_html(self.user_dc, htmx=True, htmx_mode="none", editable=True)
        self.assertNotIn("hx-trigger=", html_none)
    
    def test_theme_with_dataclasses(self):
        """Test theme support with dataclasses."""
        # Default theme
        html_default = render_html(self.user_dc)
        self.assertIn("<style>", html_default)
        
        # Light theme
        html_light = render_html(self.user_dc, theme="light")
        self.assertIn("background-color: #ffffff", html_light)
        
        # Dark theme
        html_dark = render_html(self.user_dc, theme="dark")
        self.assertIn("background-color: #1e1e1e", html_dark)
    
    def test_max_depth_with_dataclasses(self):
        """Test max_depth parameter with nested dataclasses."""
        # Test with unlimited depth
        html_full = render_html(self.user_dc)
        self.assertIn("123 Main St", html_full)
        
        # Test with depth 0 (only top level)
        html_limited = render_html(self.user_dc, max_depth=0)
        self.assertIn("UserDataClass", html_limited)
        self.assertNotIn("123 Main St", html_limited)
        self.assertIn("[Nested", html_limited)  # Should have a summary for nested model
    
    def test_complex_dataclass_rendering(self):
        """Test rendering of complex dataclass with all types."""
        html = render_html(self.complex_dc)
        
        # Check all field types
        self.assertIn("<th class=\"field-name\">string_field</th>", html)
        self.assertIn("<td class=\"field-value\">Test String</td>", html)
        
        # Number fields
        self.assertIn("<th class=\"field-name\">int_field</th>", html)
        self.assertIn("<td class=\"field-value\">50</td>", html)
        self.assertIn("<th class=\"field-name\">float_field</th>", html)
        self.assertIn("<td class=\"field-value\">0.5</td>", html)
        
        # Date field
        self.assertIn("<th class=\"field-name\">date_field</th>", html)
        self.assertIn("<td class=\"field-value\">2025-03-24</td>", html)
        
        # Enum field
        self.assertIn("<th class=\"field-name\">enum_field</th>", html)
        self.assertIn("<td class=\"field-value\">user</td>", html)
        
        # Literal field
        self.assertIn("<th class=\"field-name\">literal_field</th>", html)
        self.assertIn("<td class=\"field-value\">option2</td>", html)
        
        # List of strings
        self.assertIn("<th class=\"field-name\">list_of_strings</th>", html)
        self.assertIn("<div class=\"list-item\">one</div>", html)
        self.assertIn("<div class=\"list-item\">two</div>", html)
        self.assertIn("<div class=\"list-item\">three</div>", html)
        
        # List of models
        self.assertIn("<th class=\"field-name\">list_of_models</th>", html)
        
        # Dict field
        self.assertIn("<th class=\"field-name\">dict_field</th>", html)
        self.assertIn("key1", html)
        self.assertIn("value1", html)
        
        # Union field
        self.assertIn("<th class=\"field-name\">union_field</th>", html)
        self.assertIn("<td class=\"field-value\">string value</td>", html)
        
        # Nested model
        self.assertIn("<th class=\"field-name\">nested_model</th>", html)
        self.assertIn("123 Main St", html)
    
    def test_complex_form_rendering(self):
        """Test form rendering of complex dataclass."""
        html = render_html(self.complex_dc, editable=True)
        
        # Check form elements for different types
        self.assertIn('id="string_field"', html)
        self.assertIn('name="string_field"', html)
        self.assertIn('value="Test String"', html)
        
        self.assertIn('type="number"', html)
        self.assertIn('id="int_field"', html)
        self.assertIn('name="int_field"', html)
        self.assertIn('value="50"', html)
        
        self.assertIn('type="number"', html)
        self.assertIn('step="0.01"', html)
        self.assertIn('id="float_field"', html)
        self.assertIn('value="0.5"', html)
        
        self.assertIn('type="date"', html)
        self.assertIn('id="date_field"', html)
        self.assertIn('value="2025-03-24"', html)
        
        # Enum should be a select
        self.assertIn('id="enum_field"', html)
        self.assertIn('name="enum_field"', html)
        self.assertIn('option value="admin"', html)
        self.assertIn('option value="user" selected', html)
        
        # Literal should be a select
        self.assertIn('id="literal_field"', html)
        self.assertIn('name="literal_field"', html)
        self.assertIn('option value="option1"', html)
        self.assertIn('option value="option2" selected', html)


if __name__ == "__main__":
    unittest.main()