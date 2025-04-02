"""
Main module for blog generation.
Orchestrates the entire blog generation process.
"""
from crewai import Crew
import os

from src.utils.notebook_extractor import extract_code_and_output
from src.utils.file_handler import save_blog_content
from src.config.settings import load_environment, NOTEBOOK_PATH
from src.config.business_details import BUSINESS_NICHE, TARGET_KEYWORDS
from src.agents.agent_definitions import create_agents
from src.tasks.task_definitions import create_tasks

def generate_blog(notebook_path=NOTEBOOK_PATH):
    """
    Generate a blog post based on Jupyter notebook content.
    
    Args:
        notebook_path (str): Path to the Jupyter notebook file
        
    Returns:
        str: Generated blog content
    """
    # Load environment and initialize tools
    llm, search_tool = load_environment()
    
    # Extract notebook data
    notebook_data = " ".join(extract_code_and_output(notebook_path))
    
    # Create agents
    agents = create_agents(llm, search_tool)
    
    # Create tasks
    tasks = create_tasks(agents, notebook_data)
    
    # Create crew
    blog_crew = Crew(
        agents=list(agents),
        tasks=tasks,
        verbose=True,
        llm=llm
    )
    
    # Execute and get results
    print("Blog generation process started...")
    result = blog_crew.kickoff()
    
    # Save the result to a file
    save_blog_content(result)
    
    # Display results
    print("BLOG GENERATION COMPLETE!")
    print(f"Blog on: {BUSINESS_NICHE}")
    print(f"Keywords targeted: {TARGET_KEYWORDS}")
    print("\n--- BLOG CONTENT START ---\n")
    print(result)
    print("\n--- BLOG CONTENT END ---\n")
    
    return result

if __name__ == "__main__":
    generate_blog()
