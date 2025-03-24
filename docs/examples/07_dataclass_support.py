"""
Example showing how pydantic-to-html supports Pydantic dataclasses

This example demonstrates how the library handles both Pydantic models
and Pydantic dataclasses with the same API.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic_to_html import render_html


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


# First approach: using Pydantic BaseModel
class Address(BaseModel):
    street: str
    city: str
    zip_code: str
    country: str = "USA"


class User(BaseModel):
    name: str = Field(..., description="User's full name")
    email: str
    age: int = Field(..., gt=0, description="User's age in years")
    role: UserRole = UserRole.USER
    created_at: datetime
    address: Optional[Address] = None


# Second approach: using Pydantic dataclasses
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


def main():
    # Create some sample data
    address = Address(
        street="123 Main St",
        city="Anytown",
        zip_code="12345"
    )
    
    user = User(
        name="John Doe",
        email="john@example.com",
        age=30,
        role=UserRole.ADMIN,
        created_at=datetime.now(),
        address=address
    )
    
    # Same data as a dataclass
    address_dc = AddressDataClass(
        street="123 Main St",
        city="Anytown",
        zip_code="12345"
    )
    
    user_dc = UserDataClass(
        name="John Doe",
        email="john@example.com",
        age=30,
        created_at=datetime.now(),
        role=UserRole.ADMIN,
        address=address_dc
    )
    
    # Render both models with the same API
    html_model = render_html(user)
    html_dataclass = render_html(user_dc)
    
    # Save to files for comparison
    with open("user_model.html", "w") as f:
        f.write(html_model)
    
    with open("user_dataclass.html", "w") as f:
        f.write(html_dataclass)
    
    print("Files generated:")
    print("- user_model.html (from BaseModel)")
    print("- user_dataclass.html (from dataclass)")
    
    # You can also use the same API to create editable forms
    editable_model = render_html(user, editable=True)
    editable_dataclass = render_html(user_dc, editable=True)
    
    with open("user_model_form.html", "w") as f:
        f.write(editable_model)
    
    with open("user_dataclass_form.html", "w") as f:
        f.write(editable_dataclass)
    
    print("- user_model_form.html (editable form from BaseModel)")
    print("- user_dataclass_form.html (editable form from dataclass)")
    

if __name__ == "__main__":
    main()