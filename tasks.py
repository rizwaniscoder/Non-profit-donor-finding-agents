from crewai import Task
from textwrap import dedent

class DonorTasks:
    def __init__(self, researcher_agent, manager_agent):
        self.researcher_agent = researcher_agent
        self.manager_agent = manager_agent

    def search_donors_task(self, query):
        """
        Create a task for the researcher agent to find potential donors based on the provided query.
        """
        return Task(
            description=dedent(f"""\
                Search the web for potential donors using the query: '{query}'.
                Gather contact details, names, and a brief detail about each donor.
                Retrieve at least 50 donor records to ensure a comprehensive list.
            """),
            expected_output=dedent("""\
                A detailed list of dictionaries of at least 50 potential donors, including their contact details 
                (phone number, email, or LinkedIn), along with information about each donor. Example format:
                [
                    {"name": "John Doe", "email": "john@example.com", "phone number": "+1234567890", "detail about donor": "Here detail of the donor"},
                    {"name": "Jane Smith", "email": "smith@example.com", "phone number": "+123424347890", "detail about donor": "Here detail of the donor"},
                    // ... (at least 48 more entries)
                ]
            """),
            agent=self.researcher_agent
        )

    def analyze_donors_task(self, donors_list):
        """
        Create a task for the manager agent to analyze donor data and develop an outreach strategy.
        """
        return Task(
            description=dedent(f"""\
                Analyze the donor information provided in the list below. if the list contains information like:
                - Name
                - Email
                - Phone Number
                - Detail about donor
                then for each donor, create a custom letter
                based on their details. Ensure the letter is personalized and reflects any relevant information
                about the donor. if list not contains information like above example then give only empty list. The output should be a list of dictionaries containing:
                - Name
                - Email
                - Phone Number
                - Detail about donor
                - Custom letter

                Input donors list:
                {donors_list}
            """),
            expected_output=dedent("""\
                A list of dictionaries with the following format. For example:
                [
                    {"name": "John Doe", "email": "john@example.com", "phone number": "+1234567890", "detail about donor": "Here detail of the donor", "custom letter": "Here the custom letter text"},
                    {"name": "Jane Smith", "email": "smith@example.com", "phone number": "+123424347890", "detail about donor": "Here detail of the donor", "custom letter": "Here the custom letter text"}
                ]
            """),
            agent=self.manager_agent
        )
