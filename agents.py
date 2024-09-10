import os
from crewai import Agent
from langchain_openai import ChatOpenAI  
from langchain_community.utilities import SerpAPIWrapper
from crewai_tools import BrowserbaseLoadTool, tool


# Initialize BrowserbaseLoadTool
browserbase_tool = BrowserbaseLoadTool()
@tool("Browserbase Search Tool")
def browserbase_search_tool(url: str) -> str:
    """
    Scrapes website content using BrowserbaseLoadTool.

    Args:
        url (str): The URL of the website to be scraped.

    Returns:
        str: The scraped content from the website.
    """
    return browserbase_tool.run(url)

@tool("Search Tool")
def my_simple_tool(query: str) -> str:
    """
    Executes a search query using the SerpAPIWrapper tool and returns the result.

    Args:
        query (str): The search query to be executed.

    Returns:
        str: The result of the search query.
    """
    search = SerpAPIWrapper()
    return search.run(query)

class DonorSearchAgents:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini")  
    def researcher_agent(self):
        """
        Initializes and returns a researcher agent for finding potential donors.
        """
        search = my_simple_tool
        search_on_website = browserbase_search_tool

        
        agent = Agent(
            role='Donor Researcher',
            goal='Find potential donors and gather their contact details (phone number, email, or LinkedIn) and information about donor.',
            backstory="""You are responsible for identifying and gathering information on potential donors
            who are likely to support our non-profit organization and other detail about donor.""",
            tools=[search, search_on_website], 
            verbose=True,
            # max_iterations=100,  
            # max_execution_time=600,  
            llm=self.llm  
        )
        
        return agent

    def manager_agent(self):
        """
        Initializes and returns a manager agent for analyzing donor data.
        """
        agent = Agent(
            role='Donor Manager',
            goal='Analyze donor data and develop an outreach strategy, including writing custom letters to each donor.',
            backstory="""You will analyze the collected donor data and write personalized outreach letters to the top potential donors, 
            explaining how their contribution will help and why it’s important to support the cause.""",
            tools=[],  
            verbose=True,
            # max_iterations=100,  
            # max_execution_time=600,  
            llm=self.llm  
        )
        return agent
