import streamlit as st
from agents import DonorSearchAgents
from tasks import DonorTasks
from crewai import Crew
import os
import toml

# Load secrets and set up API keys
def load_secrets():
    try:
        secrets = toml.load("secrets.toml")
        os.environ["OPENAI_API_KEY"] = secrets["OPENAI_API_KEY"]
        os.environ["SERPAPI_API_KEY"] = secrets["SERPAPI_API_KEY"]
        os.environ["BROWSERBASE_API_KEY"] = secrets["BROWSERBASE_API_KEY"]
        os.environ["BROWSERBASE_PROJECT_ID"] = secrets["BROWSERBASE_PROJECT_ID"]
        
    except FileNotFoundError:
        st.error("The secrets.toml file was not found.")
        raise
    except KeyError as e:
        st.error(f"Missing required key in secrets.toml: {e}")
        raise
    except Exception as e:
        st.error(f"An error occurred while loading secrets: {e}")
        raise

# Initialize agents and tasks
def initialize_agents_and_tasks():
    try:
        agents = DonorSearchAgents()
        researcher_agent = agents.researcher_agent()
        manager_agent = agents.manager_agent()
        donor_tasks = DonorTasks(researcher_agent, manager_agent)
        return researcher_agent, manager_agent, donor_tasks
    except Exception as e:
        st.error(f"An error occurred while initializing agents and tasks: {e}")
        raise

# Perform donor search and return results
def search_for_donors(query, researcher_agent, donor_tasks):
    try:
        search_task = donor_tasks.search_donors_task(query)
        crew = Crew(
            agents=[researcher_agent],
            tasks=[search_task],
            verbose=True
        )
        return crew.kickoff()
    except Exception as e:
        st.error(f"An error occurred during the donor search: {e}")
        raise

# Save results to file and provide download link
def save_and_provide_download_link(results):
    try:
        filename = "Donor.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(results))
        
        with open(filename, "rb") as f:
            st.download_button(
                label="Download Donors file",
                data=f,
                file_name=filename,
                mime="text/plain"
            )
    except IOError as e:
        st.error(f"File I/O error: {e}")
    except Exception as e:
        st.error(f"Failed to save and provide download link: {e}")

# Perform donor analysis and return results
def analyze_donors(manager_agent, donor_tasks, donors_list):
    try:
        analyze_task = donor_tasks.analyze_donors_task(donors_list)
        crew = Crew(
            agents=[manager_agent],
            tasks=[analyze_task],
            verbose=True
        )
        return crew.kickoff()
    except Exception as e:
        st.error(f"An error occurred during the donor analysis: {e}")
        raise

# Main function to run the Streamlit app
def main():
    try:
        load_secrets()
        researcher_agent, manager_agent, donor_tasks = initialize_agents_and_tasks()

        st.title("Non-Profit Donor Finder")
        st.subheader("Automate the process of finding and managing potential donors for your cause")
        query = st.text_input("Enter a search query for potential donors:")

        if st.button("Search for Donors"):
            if query:
                with st.spinner('Searching for donors...'):
                    try:
                        research_result = search_for_donors(query, researcher_agent, donor_tasks)

                        if research_result:
                            st.success("Donors found successfully!")
                            st.write(research_result)
                            

                            analyze_result = analyze_donors(manager_agent, donor_tasks, research_result)
                            if analyze_result:
                                st.success("Analysis completed successfully!")
                                st.write(analyze_result)
                                save_and_provide_download_link(analyze_result)
                        else:
                            st.error("No donors found. Please try a different query.")
                    except Exception as e:
                        st.error(f"An error occurred during the search process: {e}")
            else:
                st.error("Please enter a search query.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
