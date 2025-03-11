"""
Example 6: Controlling Nested Depth

This example demonstrates how to control the depth of nested models
to prevent excessive nesting and keep the output concise.
"""

from typing import List, Optional
from pydantic import BaseModel
from pydantic_to_html import render_html


class Comment(BaseModel):
    """Comment model with author information."""
    id: int
    text: str
    author: str


class Article(BaseModel):
    """Article model with comments."""
    id: int
    title: str
    content: str
    comments: List[Comment]


class Blog(BaseModel):
    """Blog model with articles."""
    id: int
    name: str
    description: Optional[str] = None
    articles: List[Article]


def main():
    # Create a deeply nested structure
    comments = [
        Comment(id=1, text="Great article!", author="Alice"),
        Comment(id=2, text="Very informative", author="Bob"),
        Comment(id=3, text="Thanks for sharing", author="Charlie")
    ]
    
    articles = [
        Article(
            id=101, 
            title="Introduction to Pydantic", 
            content="Pydantic is a data validation library...",
            comments=comments
        ),
        Article(
            id=102, 
            title="Advanced HTML Generation", 
            content="This article covers advanced topics...",
            comments=comments[:1]  # Just one comment
        )
    ]
    
    blog = Blog(
        id=1001,
        name="Tech Blog",
        description="A blog about programming and technology",
        articles=articles
    )
    
    # Render with different depth limits
    
    # No depth limit (shows everything)
    html_full = render_html(blog)
    with open("blog_full_depth.html", "w") as f:
        f.write(html_full)
    
    # Depth limit of 1 (shows blog, but not article details)
    html_depth1 = render_html(blog, max_depth=1)
    with open("blog_depth1.html", "w") as f:
        f.write(html_depth1)
    
    # Depth limit of 2 (shows blog and articles, but not comments)
    html_depth2 = render_html(blog, max_depth=2)
    with open("blog_depth2.html", "w") as f:
        f.write(html_depth2)
    
    print("HTML files generated with different depth settings:")
    print("- blog_full_depth.html (no depth limit)")
    print("- blog_depth1.html (depth limit of 1)")
    print("- blog_depth2.html (depth limit of 2)")


if __name__ == "__main__":
    main()


"""
Expected output will show different levels of nesting based on max_depth:

1. Full depth (no limit):
   - Shows Blog
     - Shows Articles
       - Shows Comments with all details

2. Depth 1:
   - Shows Blog
     - Shows only a summary or reference to Articles, not their full details

3. Depth 2:
   - Shows Blog 
     - Shows Articles with details
       - Shows only a summary of Comments, not their full details

This control helps manage complexity, especially with large nested models,
and can significantly reduce the size of the generated HTML when needed.
"""