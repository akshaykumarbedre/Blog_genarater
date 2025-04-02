"""
Module for handling file operations.
"""

def save_blog_content(content, output_file="akshay_small_business_ai_blog.md"):
    """
    Save blog content to a file.
    
    Args:
        content (str): Blog content to save
        output_file (str): Output file path
    """
    with open(output_file, "w") as file:
        file.write(str(content))
    print(f"Blog post draft saved to {output_file}")
