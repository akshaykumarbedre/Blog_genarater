"""
Module for environment settings and API keys.
"""
import os
from dotenv import load_dotenv
from crewai import LLM
from crewai_tools import SerperDevTool

def load_environment():
    """
    Load environment variables and set API keys.
    
    Returns:
        tuple: (llm, search_tool)
    """
    # Load environment variables
    load_dotenv()
    os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
    os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

    # Initialize LLM and search tool
    llm = LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0.5,
    )
    search_tool = SerperDevTool(n=3)
    
    return llm, search_tool

# Default notebook path
NOTEBOOK_PATH = "data/demo_test.ipynb"
