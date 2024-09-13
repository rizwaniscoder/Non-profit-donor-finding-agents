from crewai import Agent
from langchain_openai import ChatOpenAI  
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

class DonorSearchAgents:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini")  
    def researcher_agent(self):
        """
        Initializes and returns a researcher agent for finding potential donors.
        """
        serper_dev_tool = SerperDevTool()
        scrape_website_tool = ScrapeWebsiteTool()
        agent = Agent(
            role='Donor Researcher',
            goal='Find potential donors and gather their contact details (phone number, email, or LinkedIn) and information about donor.',
            backstory="""You are responsible for identifying and gathering information on potential donors
            who are likely to support our non-profit organization and other detail about donor.""",
            tools=[serper_dev_tool, scrape_website_tool], 
            max_iterations=50,  
            max_rpm=100,  
            max_execution_time=3600,  # 1 hour
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
            max_iterations=50,  
            max_rpm=100,  
            max_execution_time=3600,  
            llm=self.llm  
        )
        return agent
