"""
Module containing task definitions for the blog generation process.
"""
from crewai import Task
from src.config.business_details import TARGET_KEYWORDS, BUSINESS_DETAILS

def create_tasks(agents, notebook_data):
    """
    Create and return tasks for blog generation.
    
    Args:
        agents (tuple): (data_analyst, content_creator, seo_optimizer)
        notebook_data (str): Extracted notebook data
        
    Returns:
        list: List of tasks
    """
    data_analyst, content_creator, seo_optimizer = agents
    
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
        
        Business details to incorporate: {BUSINESS_DETAILS}
        
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
        8. Naturally incorporate target keywords: {TARGET_KEYWORDS}
        9. Reflect Akshay's approach and value propositions: {BUSINESS_DETAILS['value_props']}
        
        Business details to highlight: {BUSINESS_DETAILS}

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
        2. Ensure target keywords ({TARGET_KEYWORDS}) are properly distributed throughout the content
        3. Add local SEO elements that would help Akshay rank for location-specific searches
        4. Optimize the content structure for featured snippets and voice search
        5. Include internal linking suggestions to Akshay's service pages
        6. Add FAQ schema suggestions that address common small business AI questions
        7. Suggest related blog topic ideas that would strengthen Akshay's content strategy
        
        Remember that the audience is small business owners with limited technical knowledge who
        need clear, accessible information about how AI can benefit their specific business. The
        optimization should maintain the persuasive quality of the content while improving visibility
        for relevant searches.
        
        Business details to incorporate: {BUSINESS_DETAILS}
        
        Expected output: SEO-optimized version of the blog post with specific recommendations
        for meta elements, schema markup, and a content strategy to establish Akshay as an
        authority in small business AI solutions.
        """,
        agent=seo_optimizer,
        expected_output="SEO-optimized blog post with meta elements and content strategy recommendations"
    )
    
    return [data_analysis_task, content_creation_task, seo_task]
