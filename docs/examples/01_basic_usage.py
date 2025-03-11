"""
Example 1: Basic Usage

This example demonstrates how to render a simple Pydantic model as HTML.
"""

from pydantic import BaseModel
from pydantic_to_html import render_html


class Person(BaseModel):
    """A simple person model with basic attributes."""
    name: str
    age: int
    is_active: bool


def main():
    # Create a model instance
    person = Person(name="John Doe", age=30, is_active=True)
    
    # Render it as HTML
    html = render_html(person)
    
    # Save the output to a file
    with open("person.html", "w") as f:
        f.write(html)
    
    print(f"HTML output saved to person.html")
    print("\nHTML Preview:")
    print("-------------")
    
    # Print a snippet of the output
    lines = html.split("\n")
    content_start = next(i for i, line in enumerate(lines) if "</style>" in line) + 1
    print("\n".join(lines[content_start:content_start+15]))
    print("...")


if __name__ == "__main__":
    main()


"""
Expected output will include HTML like:

<div class="pydantic-model">
  <h2 class="model-title">Person</h2>
  <div class="model-content">
    <table class="model-fields">
      <tr>
        <th class="field-name">name</th>
        <td class="field-value">John Doe</td>
      </tr>
      <tr>
        <th class="field-name">age</th>
        <td class="field-value">30</td>
      </tr>
      <tr>
        <th class="field-name">is_active</th>
        <td class="field-value">True</td>
      </tr>
    </table>
  </div>
</div>
"""