"""
Example 2: Nested Models

This example demonstrates how to render nested Pydantic models, 
including models that contain other models and lists.
"""

from typing import List, Optional
from pydantic import BaseModel
from pydantic_to_html import render_html


class Address(BaseModel):
    """Address model with basic address fields."""
    street: str
    city: str
    zip_code: str
    country: str = "USA"


class Person(BaseModel):
    """Person model with nested address and a list of tags."""
    name: str
    age: int
    address: Address
    tags: List[str]
    notes: Optional[str] = None


def main():
    # Create an address
    address = Address(
        street="123 Main St",
        city="Anytown",
        zip_code="12345"
    )
    
    # Create a person with the nested address
    person = Person(
        name="Jane Smith",
        age=28,
        address=address,
        tags=["developer", "python", "pydantic"],
        notes="Experienced developer"
    )
    
    # Render as HTML
    html = render_html(person)
    
    # Save the output
    with open("nested_person.html", "w") as f:
        f.write(html)
    
    print(f"HTML output saved to nested_person.html")
    print("\nHTML Preview:")
    print("-------------")
    
    # Print a snippet of the output
    lines = html.split("\n")
    content_start = next(i for i, line in enumerate(lines) if "</style>" in line) + 1
    preview_lines = min(25, len(lines) - content_start)
    print("\n".join(lines[content_start:content_start+preview_lines]))
    print("...")


if __name__ == "__main__":
    main()


"""
Expected output will include HTML that shows the nested structure:

<div class="pydantic-model">
  <h2 class="model-title">Person</h2>
  <div class="model-content">
    <table class="model-fields">
      <tr>
        <th class="field-name">name</th>
        <td class="field-value">Jane Smith</td>
      </tr>
      <tr>
        <th class="field-name">age</th>
        <td class="field-value">28</td>
      </tr>
      <tr>
        <th class="field-name">address</th>
        <td class="field-value field-nested">
          <table class="model-fields">
            <tr>
              <th class="field-name">street</th>
              <td class="field-value">123 Main St</td>
            </tr>
            <tr>
              <th class="field-name">city</th>
              <td class="field-value">Anytown</td>
            </tr>
            <!-- ... and so on ... -->
          </table>
        </td>
      </tr>
      <tr>
        <th class="field-name">tags</th>
        <td class="field-value field-list">
          <div class="list-item">developer</div>
          <div class="list-item">python</div>
          <div class="list-item">pydantic</div>
        </td>
      </tr>
      <tr>
        <th class="field-name">notes</th>
        <td class="field-value">Experienced developer</td>
      </tr>
    </table>
  </div>
</div>
"""