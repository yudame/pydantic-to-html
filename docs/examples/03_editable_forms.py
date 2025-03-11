"""
Example 3: Editable Forms

This example demonstrates how to generate editable HTML forms 
from Pydantic models with the `editable=True` option.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_to_html import render_html


class UserProfile(BaseModel):
    """User profile model with various field types to demonstrate form inputs."""
    username: str = Field(..., min_length=3, max_length=20)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    age: int = Field(..., gt=0, lt=120)
    bio: Optional[str] = Field(None, max_length=500)
    is_active: bool = True
    last_login: datetime = Field(default_factory=datetime.now)
    interests: List[str] = []


def main():
    # Create a model instance
    user = UserProfile(
        username="johndoe",
        email="john@example.com",
        age=35,
        bio="Software developer and tech enthusiast",
        interests=["programming", "hiking", "photography"]
    )
    
    # Render as an editable HTML form
    html = render_html(user, editable=True)
    
    # Save the output
    with open("user_form.html", "w") as f:
        f.write(html)
    
    print(f"HTML form saved to user_form.html")
    print("\nHTML Preview:")
    print("-------------")
    
    # Print a snippet of the output
    lines = html.split("\n")
    content_start = next(i for i, line in enumerate(lines) if "</style>" in line) + 1
    preview_lines = min(30, len(lines) - content_start)
    print("\n".join(lines[content_start:content_start+preview_lines]))
    print("...")


if __name__ == "__main__":
    main()


"""
Expected output will include HTML form elements with input fields:

<form class="pydantic-model-form">
  <h2 class="model-title">UserProfile</h2>
  <div class="model-content">
    <fieldset class="model-fields">
      <div class="form-field">
        <label for="username">username</label>
        <input type="text" id="username" name="username" 
               minlength="3" maxlength="20" value="johndoe" required>
      </div>
      <div class="form-field">
        <label for="email">email</label>
        <input type="text" id="email" name="email" 
               pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" 
               value="john@example.com" required>
      </div>
      <div class="form-field">
        <label for="age">age</label>
        <input type="number" step="1" id="age" name="age" 
               min="1" max="119" value="35" required>
      </div>
      <!-- Additional fields omitted for brevity -->
    </fieldset>
    <div class="form-actions">
      <button type="submit" class="submit-button">Submit</button>
    </div>
  </div>
</form>
"""