"""
Example 5: HTMX Integration

This example demonstrates how to use the HTMX integration features
to create dynamic, interactive HTML from Pydantic models.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_to_html import render_html


class TaskStatus(str, Enum):
    """Task status enum."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(BaseModel):
    """Task model for a simple task management system."""
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: int = Field(1, ge=1, le=5)
    tags: List[str] = []


def main():
    # Create some task instances
    task = Task(
        id=1,
        title="Implement HTMX examples",
        description="Create a sample showing HTMX integration",
        status=TaskStatus.IN_PROGRESS,
        priority=3,
        tags=["documentation", "example", "htmx"]
    )
    
    # Basic view with HTMX for automatic refreshing
    html_auto_refresh = render_html(task, htmx=True)
    with open("task_auto_refresh.html", "w") as f:
        f.write(html_auto_refresh)
    
    # Editable form with HTMX full mode (auto-submit on change)
    html_full_mode = render_html(task, editable=True, htmx=True, htmx_mode="full")
    with open("task_form_full.html", "w") as f:
        f.write(html_full_mode)
    
    # Editable form with HTMX inline mode (update specific fields)
    html_inline_mode = render_html(task, editable=True, htmx=True, htmx_mode="inline")
    with open("task_form_inline.html", "w") as f:
        f.write(html_inline_mode)
    
    print("HTML files generated with HTMX integration:")
    print("- task_auto_refresh.html (auto-refreshing view)")
    print("- task_form_full.html (form with full auto-submit)")
    print("- task_form_inline.html (form with inline field updates)")
    
    # Print information about how HTMX attributes were added
    print("\nExample HTMX Attributes:")
    print("------------------------")
    print("Auto-refresh: hx-get=\"/refresh\" hx-trigger=\"every 10s\"")
    print("Full form mode: hx-post=\"/submit\" hx-trigger=\"change delay:500ms\"")
    print("Inline mode: Input fields have hx-trigger=\"change\" hx-post=\"/update-field\"")


if __name__ == "__main__":
    main()


"""
Expected output will include HTML with HTMX attributes:

1. Auto-refreshing view example:
<div class="pydantic-model" hx-get="/refresh" hx-trigger="every 10s">
  <!-- Model content -->
</div>

2. Form with full auto-submit example:
<form class="pydantic-model-form" hx-post="/submit" hx-trigger="change delay:500ms">
  <!-- Form fields -->
</form>

3. Form with inline field updates example:
<form class="pydantic-model-form">
  <div class="form-field">
    <label for="title">title</label>
    <input type="text" id="title" name="title" value="Implement HTMX examples" 
           hx-trigger="change" hx-post="/update-field">
  </div>
  <!-- More form fields -->
</form>
"""