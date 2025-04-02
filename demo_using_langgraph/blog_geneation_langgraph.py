# %%
from juputer_data_extracter import extract_code_and_output
from model_llm import llm_google
from typing_extensions import TypedDict,List ,Dict,Literal
from pydantic import BaseModel, Field
path=r"data\demo_test.ipynb"


class BlogGeneratorState(TypedDict):
    path: str
    notebook_content: str
    parsed_code: str
    draft_blog: str
    feedback: str
    accept_or_reject: str
    final_blog: str



# %%
def parse_nodebook(state:BlogGeneratorState):
    path=state["path"]
    notebook_content="\n---\n".join(extract_code_and_output(path))
    return {"notebook_content":notebook_content}

# %%
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage , HumanMessage , AnyMessage
prompt_parse_code = ChatPromptTemplate.from_template("""
    You are a code parsing assistant. Your task is to clean raw Jupyter Notebook cell code by removing unnecessary symbols, comments, and irrelevant content, preserving only the essential code.
    The cleaned code should maintain its original structure and logic without adding any extra content.
    
    Raw Jupyter code:
    {notebook_content}
    
    Provide the cleaned code and its output in the following format for each cell:
    
    ```
    <cleaned_code>
    output: <sample_output_of_cleaned_code upto 200 characters then show ...>
    ```
""")


def parse_code(state:BlogGeneratorState):
    notebook_content=state["notebook_content"]
    Parse_chain=prompt_parse_code|llm_google
    Parse_ouput=Parse_chain.invoke({"notebook_content":notebook_content})
    return {"parsed_code":Parse_ouput.content}

# %%
prompt_generate_blog = ChatPromptTemplate.from_template("""
    You are a blog generation assistant. Your task is to create an engaging, beginner-friendly, and SEO-optimized blog post using the parsed Jupyter Notebook code provided.
    
    Parsed code with sample output:
    {parsed_code}
    
    Guidelines for blog generation:
    - Provide a clear and concise introduction explaining the objective of the code.
    - Break down the code into meaningful sections with appropriate headings.
    - Explain each section in simple terms, making it easy for beginners to understand.
    - Include the cleaned code and its sample output for each cell in the following format:
    
    ```python
    # Brief comments explaining the code.
    <cleaned_python_code>
    ```

    **Output:**
    ```
    <sample_output_of_cleaned_code>
    ```

    - Highlight key concepts or techniques used in the code.
    - Incorporate relevant SEO-friendly keywords naturally throughout the content.
    - Conclude with a summary that reinforces the learnings and encourages further exploration.

    Ensure that the blog is:
    - Well-structured with appropriate headings and subheadings.
    - Informative, easy to follow, and visually appealing.
    - Optimized for SEO to enhance visibility in search engines.
                                                        
                                                        
""")

prompt_generate_blog_feedback = ChatPromptTemplate.from_template("""
    You are a blog refinement assistant. Your task is to improve an existing blog post based on the provided feedback to enhance its quality, clarity, and SEO optimization.
    
    Existing blog content:
    {parsed_code}
    
    Feedback:
    ```
    {feedback}
    ```

    Guidelines for refining the blog:
    - Address all points mentioned in the feedback to improve readability, structure, and SEO optimization.
    - Simplify any complex explanations to make the content more beginner-friendly.
    - Ensure relevant SEO keywords are naturally incorporated.
    - Maintain proper code formatting and output display.
    - Add missing sections or concepts if mentioned in the feedback.
    
    Provide the refined blog content with improvements incorporated.
""")


def generate_blog(state:BlogGeneratorState):
    if state.get("feedback"):
        
        parsed_code=state["parsed_code"]
        Feedback=state["feedback"]
        Generate_chain=prompt_generate_blog_feedback|llm_google
        Generate_output=Generate_chain.invoke({"parsed_code":parsed_code,"feedback":Feedback})
        # Generate_output=llm.invoke(f"genarate joke about {state['topic']} while considering the feedback {state['feedback']}")
        return {"draft_blog":Generate_output.content}
    else:
        parsed_code=state["parsed_code"]
        Generate_chain=prompt_generate_blog|llm_google
        Generate_output=Generate_chain.invoke({"parsed_code":parsed_code})
        return {"draft_blog":Generate_output.content} 


# %%
from pydantic import BaseModel, Field
from typing_extensions import Literal

class Feedback(BaseModel):
    accept_or_reject: Literal["Approved", "Rejected"] = Field(
        description="Review status of the generated blog content. 'Approved' if the content is clear and SEO optimized, 'Rejected' if improvements are needed."
    )
    feedback: str = Field(
        description="Detailed feedback on whether the blog is beginner-friendly, easy to understand, and optimized for SEO. Include suggestions for improvement if necessary."
    )

# LLM with structured feedback output
feedback_llm_prompt = ChatPromptTemplate.from_template("""
    You are a blog review assistant. Your task is to evaluate a blog post based on its quality, readability, and SEO optimization.
    
    Blog content:
    {draft_blog}
    
    Guidelines for feedback:
    - Approve the blog if it is beginner-friendly, SEO optimized, and easy to understand.
    - Reject the blog if improvements are needed and provide detailed suggestions for enhancement.
    - Highlight any missing sections, technical inaccuracies, or SEO-related improvements.
    
    Provide the feedback in the following format:
    - accept_or_reject: "Approved" or "Rejected"
    - feedback: A detailed review with suggestions for improvement.
""")

# Integrate prompt with LLM for structured feedback
feedback_llm = feedback_llm_prompt | llm_google.with_structured_output(Feedback)

# Feedback function to evaluate the blog
def feedback(state: BlogGeneratorState):
    draft_blog = state["draft_blog"]
    
    # Invoke feedback with draft blog content
    feedback_response = feedback_llm.invoke({"draft_blog": draft_blog})
    
    # Return feedback and status
    return {
        "feedback": feedback_response.feedback,
        "accept_or_reject": feedback_response.accept_or_reject
    }

def joke_condition(state):
    if state['accept_or_reject']=="Approved":
        return "Approved"
    else :
        return "Rejected+Feedback"

# %%
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph, END
from IPython.display import Markdown, display

# Create the state graph
def create_blog_generator_graph():
    # Initialize the graph with the defined state
    workflow = StateGraph(BlogGeneratorState)
    
    # Add nodes to the graph
    workflow.add_node("parse_notebook", parse_nodebook)
    workflow.add_node("parse_code", parse_code)
    workflow.add_node("generate_blog", generate_blog)
    workflow.add_node("feedback", feedback)
    
    # Define edges connecting the nodes
    workflow.add_edge("parse_notebook", "parse_code")
    workflow.add_edge("parse_code", "generate_blog")
    workflow.add_edge("generate_blog", "feedback")
    
    # Add conditional edge from feedback
    workflow.add_conditional_edges(
        "feedback",
        joke_condition,
        {
            "Approved": END,
            "Rejected+Feedback": "generate_blog"
        }
    )
    
    # Set the entry point
    workflow.set_entry_point("parse_notebook")
    
    # Compile the graph
    return workflow.compile()

# Function to run the blog generator with a notebook path
def generate_blog_from_notebook(notebook_path):
    # Create the graph
    blog_generator = create_blog_generator_graph()
    
    # Initialize the state
    initial_state = {"path": notebook_path}
    
    # Execute the graph
    result = blog_generator.invoke(initial_state)
    
    # Return the final state containing the blog
    return result

# Function to display the generated blog
def display_blog(result):
    if result.get("accept_or_reject") == "Approved":
        display(Markdown("## Final Blog Post"))
        display(Markdown(result["draft_blog"]))
        return result["draft_blog"]
    else:
        print("Blog generation is still in progress or was not approved.")
        return None

# Example usage
if __name__ == "__main__":
    result = generate_blog_from_notebook(path)
    final_blog = display_blog(result)

# %%



