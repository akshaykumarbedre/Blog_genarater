from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os
import os
from dotenv import load_dotenv
load_dotenv() 

os.environ['GITHUB_TOKEN']=os.getenv('GITHUB_TOKEN')
os.environ['GOOGLE_API_KEY']=os.getenv('GEMINI_API_KEY')

endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"
# Initialize the LangChain chat model with the same parameters
llm_openai = ChatOpenAI(
    model=model_name,
    temperature=1.0,
    max_tokens=1000,
    top_p=1.0,
    openai_api_key=os.environ['GITHUB_TOKEN'],
    openai_api_base=endpoint
)

from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize the LangChain chat model with the same parameters
llm_google = ChatGoogleGenerativeAI(model="gemini-2.0-flash")