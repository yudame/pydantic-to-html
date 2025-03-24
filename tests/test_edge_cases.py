"""
Tests for edge cases and special situations in both BaseModel and dataclasses
"""

import unittest
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass as pydantic_dataclass

from pydantic_to_html import render_html


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


# 1. Test empty collections
class EmptyCollectionsModel(BaseModel):
    empty_list: List[str] = []
    empty_dict: Dict[str, Any] = {}
    none_value: Optional[str] = None


@pydantic_dataclass
class EmptyCollectionsDataClass:
    empty_list: List[str] = Field(default_factory=list)
    empty_dict: Dict[str, Any] = Field(default_factory=dict)
    none_value: Optional[str] = None


# 2. Test with bytes and callables (unsupported types)
def dummy_function():
    return "Hello"


class UnsupportedTypesModel(BaseModel):
    bytes_data: bytes = b"binary data"
    callable_data: Any = dummy_function


@pydantic_dataclass
class UnsupportedTypesDataClass:
    bytes_data: bytes = b"binary data"
    callable_data: Any = dummy_function


# 3. Test with unusual values (very long strings, extreme numbers)
class ExtremeCasesModel(BaseModel):
    long_string: str = "a" * 1000
    large_number: int = 10**10
    very_small_float: float = 1.23e-10


@pydantic_dataclass
class ExtremeCasesDataClass:
    long_string: str = "a" * 1000
    large_number: int = 10**10
    very_small_float: float = 1.23e-10


class TestEdgeCases(unittest.TestCase):
    def test_empty_collections_basemodel(self):
        """Test rendering of empty collections in BaseModel."""
        model = EmptyCollectionsModel()
        html = render_html(model)
        
        self.assertIn("<h2 class=\"model-title\">EmptyCollectionsModel</h2>", html)
        
        # Empty list should still be rendered
        self.assertIn("<th class=\"field-name\">empty_list</th>", html)
        self.assertIn("<td class=\"field-value field-list\">", html)
        
        # Empty dict should be rendered as an empty table
        self.assertIn("<th class=\"field-name\">empty_dict</th>", html)
        self.assertIn("<td class=\"field-value field-nested\">", html)
        
        # None value should be rendered as "None"
        self.assertIn("<th class=\"field-name\">none_value</th>", html)
        self.assertIn("<td class=\"field-value\">None</td>", html)
    
    def test_empty_collections_dataclass(self):
        """Test rendering of empty collections in dataclass."""
        model = EmptyCollectionsDataClass()
        html = render_html(model)
        
        self.assertIn("<h2 class=\"model-title\">EmptyCollectionsDataClass</h2>", html)
        
        # Empty list should still be rendered
        self.assertIn("<th class=\"field-name\">empty_list</th>", html)
        
        # Empty dict should be rendered properly
        self.assertIn("<th class=\"field-name\">empty_dict</th>", html)
        
        # None value should be rendered as "None"
        self.assertIn("<th class=\"field-name\">none_value</th>", html)
        self.assertIn("<td class=\"field-value\">None</td>", html)
    
    def test_unsupported_types_basemodel(self):
        """Test rendering of unsupported types in BaseModel."""
        model = UnsupportedTypesModel()
        html = render_html(model)
        
        # Bytes should be rendered as string representation
        self.assertIn("<th class=\"field-name\">bytes_data</th>", html)
        self.assertIn("binary data", html)
        
        # Callable should be rendered as string representation
        self.assertIn("<th class=\"field-name\">callable_data</th>", html)
        self.assertIn("<td class=\"field-value\">", html)
        self.assertIn("function", html.lower())  # Function representation varies
    
    def test_unsupported_types_dataclass(self):
        """Test rendering of unsupported types in dataclass."""
        model = UnsupportedTypesDataClass()
        html = render_html(model)
        
        # Bytes should be rendered as string representation
        self.assertIn("<th class=\"field-name\">bytes_data</th>", html)
        self.assertIn("binary data", html)
        
        # Callable should be rendered as string representation
        self.assertIn("<th class=\"field-name\">callable_data</th>", html)
        self.assertIn("<td class=\"field-value\">", html)
        self.assertIn("function", html.lower())  # Function representation varies
    
    def test_extreme_cases_basemodel(self):
        """Test rendering of extreme values in BaseModel."""
        model = ExtremeCasesModel()
        html = render_html(model)
        
        # Long string should be rendered properly
        self.assertIn("<th class=\"field-name\">long_string</th>", html)
        self.assertIn("a" * 100, html)  # At least part of the long string should be there
        
        # Large number should be rendered properly
        self.assertIn("<th class=\"field-name\">large_number</th>", html)
        self.assertIn("<td class=\"field-value\">10000000000</td>", html)
        
        # Small float should be rendered properly
        self.assertIn("<th class=\"field-name\">very_small_float</th>", html)
        self.assertIn("<td class=\"field-value\">1.23e-10</td>", html)
    
    def test_extreme_cases_dataclass(self):
        """Test rendering of extreme values in dataclass."""
        model = ExtremeCasesDataClass()
        html = render_html(model)
        
        # Long string should be rendered properly
        self.assertIn("<th class=\"field-name\">long_string</th>", html)
        self.assertIn("a" * 100, html)  # At least part of the long string should be there
        
        # Large number should be rendered properly
        self.assertIn("<th class=\"field-name\">large_number</th>", html)
        self.assertIn("<td class=\"field-value\">10000000000</td>", html)
        
        # Small float should be rendered properly
        self.assertIn("<th class=\"field-name\">very_small_float</th>", html)
        self.assertIn("<td class=\"field-value\">1.23e-10</td>", html)
    
    def test_edge_cases_in_form(self):
        """Test rendering edge cases as forms."""
        model_empty = EmptyCollectionsDataClass()
        html_empty = render_html(model_empty, editable=True)
        
        # Test form field for empty list
        self.assertIn('id="empty_list"', html_empty)
        self.assertIn('name="empty_list"', html_empty)
        
        # Test form field for None value
        self.assertIn('id="none_value"', html_empty)
        self.assertIn('name="none_value"', html_empty)
        self.assertIn('value=""', html_empty)  # None should be an empty string in forms
        
        # Test extreme values in forms
        model_extreme = ExtremeCasesDataClass()
        html_extreme = render_html(model_extreme, editable=True)
        
        # Long string should be properly escaped in form
        self.assertIn('id="long_string"', html_extreme)
        self.assertIn('name="long_string"', html_extreme)
        self.assertIn('value="' + "a" * 100, html_extreme)  # At least part of it
        
        # Large number should be in form
        self.assertIn('id="large_number"', html_extreme)
        self.assertIn('name="large_number"', html_extreme)
        self.assertIn('value="10000000000"', html_extreme)


if __name__ == "__main__":
    unittest.main()