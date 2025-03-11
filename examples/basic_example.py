"""
Basic example showing how to use pydantic-to-html
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_to_html import model_to_html, render_html


class Address(BaseModel):
    street: str
    city: str
    zip_code: str
    country: str = "USA"


class User(BaseModel):
    name: str = Field(..., description="User's full name")
    email: str
    age: int = Field(..., gt=0, description="User's age in years")
    is_active: bool = True
    tags: List[str] = []
    address: Optional[Address] = None


def main():
    # Create a user with nested address
    address = Address(
        street="123 Main St",
        city="Anytown",
        zip_code="12345"
    )
    
    user = User(
        name="John Doe",
        email="john@example.com",
        age=30,
        tags=["customer", "premium", "verified"],
        address=address
    )
    
    # Convert to HTML using the new API
    html = render_html(user)
    
    # Save to a file
    with open("user.html", "w") as f:
        f.write(html)
    
    print(f"HTML generated and saved to user.html")
    
    # You can also use the legacy API
    html_legacy = model_to_html(user)
    
    # Generate HTML without CSS
    html_without_css = model_to_html(user, include_css=False)
    
    # Or with custom CSS
    custom_css = """
    .pydantic-model {
        font-family: Arial, sans-serif;
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
    }
    .model-title {
        color: navy;
    }
    .field-name {
        color: #444;
    }
    """
    html_with_custom_css = model_to_html(user, custom_css=custom_css)
    
    # Using the new API with options
    html_with_options = render_html(
        user,
        editable=True,  # Will be implemented in future versions
        theme="light",  # Will be implemented in future versions
        htmx=True,      # Will be implemented in future versions
        htmx_mode="inline"
    )
    
    with open("user_with_options.html", "w") as f:
        f.write(html_with_options)
    
    print("Examples complete!")


if __name__ == "__main__":
    main()