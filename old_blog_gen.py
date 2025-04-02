from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv


import nbformat
from langchain.schema import Document


def extract_code_and_output(notebook_path):
    try:
        # Load the notebook
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        documents = []

        # Iterate through notebook cells
        for cell in notebook.cells:
            if cell.cell_type == "code":
                code_content = "\n".join(cell.source.splitlines())
                output_content = []
                
                if hasattr(cell, 'outputs'):
                    for output in cell.outputs:
                        if "text" in output:
                            output_content.append(output["text"])
                        elif "data" in output and "text/plain" in output["data"]:
                            output_content.append(output["data"]["text/plain"])
                        elif "ename" in output and "evalue" in output:
                            error_msg = f"{output['ename']}: {output['evalue']}"
                            output_content.append(error_msg)

                # Prepare document format
                document_content = f"'code' cell: {repr(code_content)}"
                if output_content:
                    document_content += f"\n with output: {repr(output_content)}"
                else:
                    document_content += "\n with output: []"

                # Add to documents list
                doc = Document(
                    page_content=document_content,
                   
                )
                documents.append(document_content)

        return documents

    except Exception as e:
        print(f"Error while processing notebook: {str(e)}")
        return []


# Load environment variables and set API keys
load_dotenv()
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Initialize LLM and search tool
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.5,
)
search_tool = SerperDevTool(n=3)

# Define notebook data (this would be your Jupyter notebook output)
notebook_data = " ".join(extract_code_and_output("data/demo_test.ipynb"))

# Define target keywords and business niche based on Akshay's business
target_keywords = ["AI for small business", "Affordable chatbots", "Business automation", "Custom AI solutions", "Small business analytics"]
business_niche = "Affordable AI Solutions for Small Businesses"

# Define business details for content
business_details = {
    "name": "Akshay Kumar BM",
    "focus": "Affordable AI solutions for small businesses",
    "services": {
        "chatbots": "24/7 customer service chatbots starting at ₹25,000",
        "automation": "Business process automation starting at ₹30,000",
        "analytics": "Small business analytics dashboards starting at ₹20,000",
        "integrations": "Custom AI integrations starting at ₹35,000"
    },
    "value_props": [
        "Budget-friendly AI solutions",
        "Quick implementation in 2-4 weeks",
        "No technical knowledge required",
        "Clear ROI and measurable results",
        "Integration with existing systems",
        "Ongoing support and training"
    ],
    "contact": "akshaykumarbm.aifx@gmail.com"
}

# Create agents
data_analyst = Agent(
    role="AI Solutions Research Specialist",
    goal="Extract valuable insights about AI solutions for small businesses and identify key use cases and benefits",
    backstory="""You are an expert in AI technology with a focus on practical applications for small businesses.
    You excel at understanding how emerging AI tools can solve real business problems while fitting within
    small business budgets and technical capabilities. Your research identifies the most valuable and accessible 
    AI solutions that deliver tangible ROI for small business owners.
    
    Your specific task is to analyze data from Jupyter notebooks and other sources to identify key trends,
    use cases, and implementation strategies for AI in small business environments. You focus particularly on
    chatbots, process automation, analytics, and AI integrations - all tailored to the needs and constraints
    of small businesses that can't afford enterprise solutions.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

content_creator = Agent(
    role="Small Business AI Content Strategist",
    goal="Create engaging, informative blog content that demonstrates expertise in affordable AI solutions while addressing small business pain points",
    backstory="""You are a talented content creator specializing in explaining AI technology to non-technical
    small business audiences. You have years of experience translating complex technical concepts into
    accessible, value-focused content that resonates with small business owners.
    
    You understand that small business owners are primarily concerned with ROI, implementation time,
    ease of use, and competitive advantage - not technical specifications. Your writing makes AI 
    approachable by focusing on concrete benefits, real-world applications, and success stories.
    
    You excel at creating content that positions AI specialists as trusted advisors who understand
    the unique challenges of small businesses and can provide custom solutions that deliver immediate value.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

seo_optimizer = Agent(
    role="Small Business AI SEO Specialist",
    goal="Optimize blog content to attract small business owners searching for affordable AI solutions",
    backstory="""You are an SEO expert who specializes in helping AI consultants and developers reach
    small business audiences. You understand the search behavior of small business owners looking for
    technology solutions - their concerns, questions, and terminology.
    
    You know exactly how to structure content, incorporate keywords naturally, and optimize meta elements
    to achieve maximum visibility for local and specialized AI service providers. You balance technical
    SEO requirements with persuasive content that builds trust and encourages consultation bookings.
    
    You're skilled at incorporating local SEO elements, service-specific keywords, and trust signals
    that help independent AI consultants compete with larger agencies and platforms.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

# Create tasks
data_analysis_task = Task(
    description=f"""Analyze the provided Jupyter notebook data and conduct additional research to identify
    the most valuable and accessible AI applications for small businesses in 2025. Focus on solutions that
    align with Akshay Kumar BM's service offerings and expertise.
    
    Notebook data: {notebook_data}
    
    Conduct thorough research on:
    1. Current trends in small business AI adoption, focusing on chatbots, automation, analytics, and integrations
    2. Common small business problems that can be solved with affordable AI solutions
    3. Implementation strategies that work within small business constraints (budget, technical capabilities, time)
    4. Competitive advantages AI provides to small businesses competing with larger enterprises
    5. Case studies and success metrics from small businesses using AI solutions similar to Akshay's offerings
    
    Business details to incorporate: {business_details}
    
    Expected output: A comprehensive analysis including:
    1. Key small business pain points that Akshay's AI solutions can address
    2. Specific use cases for each service offering with clear benefit statements
    3. Implementation insights that demonstrate Akshay's expertise and approach
    4. Data points and statistics that build credibility for small business AI solutions
    5. Unique selling propositions that differentiate Akshay from larger AI providers
    """,
    agent=data_analyst,
    expected_output="Detailed research report on small business AI applications and benefits"
)

content_creation_task = Task(
    description=f"""Using the research findings, create a comprehensive, persuasive blog post that
    positions Akshay Kumar BM as an expert in affordable AI solutions for small businesses. The post
    should educate small business owners about practical AI applications while subtly promoting
    Akshay's services.
    
    Your blog post should:
    1. Have an attention-grabbing title that addresses a key small business pain point
    2. Open with a relatable scenario that illustrates the challenges small businesses face
    3. Explain AI solutions in accessible, benefit-focused language for non-technical audiences
    4. Include specific examples of how each of Akshay's services solves real business problems
    5. Incorporate success metrics and mini case studies that build credibility
    6. Address common objections (cost, complexity, implementation time)
    7. Include a compelling call-to-action for the free consultation
    8. Naturally incorporate target keywords: {target_keywords}
    9. Reflect Akshay's approach and value propositions: {business_details['value_props']}
    
    Business details to highlight: {business_details}

    Expected output: A well-structured, persuasive blog post of 1200-1500 words that generates
    interest in Akshay's AI services and positions him as a trusted advisor to small businesses.
    """,
    agent=content_creator,
    expected_output="Complete blog post draft that positions Akshay as a small business AI expert"
)

seo_task = Task(
    description=f"""Optimize the blog draft to attract small business owners searching for affordable
    AI solutions in India, with particular focus on Bengaluru and surrounding areas. Ensure the content
    ranks well for Akshay Kumar BM's target keywords while maintaining its persuasive quality.
    
    1. Create an SEO-optimized title, meta description, and heading structure
    2. Ensure target keywords ({target_keywords}) are properly distributed throughout the content
    3. Add local SEO elements that would help Akshay rank for location-specific searches
    4. Optimize the content structure for featured snippets and voice search
    5. Include internal linking suggestions to Akshay's service pages
    6. Add FAQ schema suggestions that address common small business AI questions
    7. Suggest related blog topic ideas that would strengthen Akshay's content strategy
    
    Remember that the audience is small business owners with limited technical knowledge who
    need clear, accessible information about how AI can benefit their specific business. The
    optimization should maintain the persuasive quality of the content while improving visibility
    for relevant searches.
    
    Business details to incorporate: {business_details}
    
    Expected output: SEO-optimized version of the blog post with specific recommendations
    for meta elements, schema markup, and a content strategy to establish Akshay as an
    authority in small business AI solutions.
    """,
    agent=seo_optimizer,
    expected_output="SEO-optimized blog post with meta elements and content strategy recommendations"
)

# Create and run the crew
blog_crew = Crew(
    agents=[data_analyst, content_creator, seo_optimizer],
    tasks=[data_analysis_task, content_creation_task, seo_task],
    verbose=True,
    llm=llm
)

# Execute and get results
result = blog_crew.kickoff()

print("Blog generation process started...")
# Notify user of completion
print(result)
# Save the result to a file
output_file = "akshay_small_business_ai_blog.md"
with open(output_file, "w") as file:
    file.write(str(result))
# Notify user of completion
print(f"Blog post draft saved to {output_file}")
print("Blog generation process completed successfully!")

# Display results
print("BLOG GENERATION COMPLETE!")
print(f"Blog on: {business_niche}")
print(f"Keywords targeted: {target_keywords}")
print("\n--- BLOG CONTENT START ---\n")
print(result)
print("\n--- BLOG CONTENT END ---\n")