"""
Example 4: Themes and Styling

This example demonstrates how to use different themes and custom CSS
to style the HTML output generated from Pydantic models.
"""

from pydantic import BaseModel
from pydantic_to_html import render_html


class Product(BaseModel):
    """A simple product model."""
    name: str
    price: float
    description: str
    in_stock: bool


def main():
    # Create a product instance
    product = Product(
        name="Ergonomic Keyboard", 
        price=129.99, 
        description="A comfortable keyboard for long coding sessions",
        in_stock=True
    )
    
    # Default styling
    default_html = render_html(product)
    with open("product_default.html", "w") as f:
        f.write(default_html)
    
    # Light theme
    light_html = render_html(product, theme="light")
    with open("product_light.html", "w") as f:
        f.write(light_html)
    
    # Dark theme
    dark_html = render_html(product, theme="dark")
    with open("product_dark.html", "w") as f:
        f.write(dark_html)
    
    # Custom CSS
    custom_css = """
    .pydantic-model {
        font-family: 'Georgia', serif;
        background-color: #f8f9fa;
        border: 2px solid #6c757d;
        border-radius: 10px;
        padding: 20px;
        max-width: 800px;
        margin: 20px auto;
    }
    .model-title {
        color: #495057;
        border-bottom: 2px solid #6c757d;
        padding-bottom: 10px;
        font-size: 24px;
        text-align: center;
    }
    .field-name {
        color: #495057;
        font-weight: bold;
        width: 40%;
    }
    .field-value {
        color: #212529;
        font-family: 'Courier New', monospace;
    }
    """
    
    custom_html = render_html(
        product, 
        include_css=True, 
        custom_css=custom_css
    )
    with open("product_custom.html", "w") as f:
        f.write(custom_html)
    
    print("HTML files generated with different themes:")
    print("- product_default.html (default styling)")
    print("- product_light.html (light theme)")
    print("- product_dark.html (dark theme)")
    print("- product_custom.html (custom CSS)")


if __name__ == "__main__":
    main()


"""
Expected output will include HTML with different styling based on the theme:

1. Default theme: Standard styling with neutral colors
2. Light theme: Clean design with lighter colors, subtle borders, and more white space
3. Dark theme: Dark background with light text for low-light conditions
4. Custom CSS: Complete control over the styling with user-defined CSS

Each theme provides the same structured HTML but with different visual styling,
making it easy to integrate with various web applications and designs.
"""