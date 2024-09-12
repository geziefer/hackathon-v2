from langchain.agents import tool
from typing import List, Dict
import requests
from langchain_community.retrievers import AzureCognitiveSearchRetriever
import os
import config

"""
This file holds the tools, that can be bound to the AgentExecutor object.
Here, we define new functions that the agent can invoke and that help it to solve the tasks. These functions
can, e.g., include database operations, real time log queries, control of the factory, etc.
Be careful though, the AI itself decides, based on the provided docstring, which tool to invoke and what
parameters to pass! So carefully consider, which tools you want to add... ;)
"""


### HELP-TOOL: GET INFORMATION ABOUT THE DATABASE ###


@tool
def get_db_info() -> str:
    """
    This function can be used to retrieve information about the database, that can be accessed.
    It returns a text describing the database's structure for the user.

    Returns:
        str: text, describing the database-structure
    """

    return config.DATABASE_DESCR


### TASK 1: GET IIOT DATA (input, ambient, machine, qa) ###


@tool()
def get_machine_data(
        from_timestamp: str | None,
        to_timestamp: str | None,
        min_material_temperature: float | None,
        max_material_temperature: float | None,
        min_motor_rpm: float | None,
        max_motor_rpm: float | None,
) -> Dict[str, str]:
    """
    This function can be used to get or retrieve machine data like RPM , pressure, temperature, etc

    Args:
        from_timestamp (str | None): Start Timestamp
        to_timestamp (str | None): End Timestamp
        min_material_temperature (float | None): Minimum temperature of material
        max_material_temperature (float | None): Maximum temperature of material
        min_motor_rpm (float | None): Minimum RPM of motor
        max_motor_rpm (float | None): Maximum RPM of motor

    Returns:
        Dict[str, str]: Returns a List of machine data in JSON dictionary format.
        Each entry has an id , timestamp and set of properties like RPM , pressure, temperature, etc
    """

    # Prepare the URL to call the Factory's API (Note: use config.BACKEND_URL)
    url = 'http://4.182.189.203:8080/machine'

    params = {
        'from_ts': from_timestamp,
        'to_ts': to_timestamp,
        'min_material_temperature': min_material_temperature,
        'max_material_temperature': max_material_temperature,
        'min_motor_rpm': min_motor_rpm,
        'max_motor_rpm': max_motor_rpm,
    }

    # Send the request to get the data from the machine endpoint
    response = requests.get(url, params)
    machine_data_dict: Dict[str, str] = response.json()
    limited_data = machine_data_dict[:100]

    # Optional: Postprocess the data to be in your desired format
    return limited_data


# Question: Do you need to invoke the API Endpoints for the other tables as well? (input, ambient, qa)


### TASK 2: QUERY LOGS-API-ENDPOINT ###


@tool
def get_logs(
        from_timestamp: str | None, to_timestamp: str | None
) -> List[Dict[str, str]]:
    """
    ### Description of the function
    ### IMPORTANT! The LLM decides to call it or not based on this docstring!

    Args:
        from_timestamp (str | None): ...
        to_timestamp (str | None): ...

    Returns:
        List[Dict[str, str]]: ...
    """

    # Prepare the URL to call the Factory's API
    pass

    # Send the request to get the data from the logs endpoint
    pass

    # Optional: Postprocess the data to be in your desired format
    pass

    return []


### TASK 3: QUERY DOCUMENTATION USING RAG ###


@tool
def query_documentation(question: str) -> str:
    """
    ### Description of the function
    ### IMPORTANT! The LLM decides to call it or not based on this docstring!

    Args:
        question (str): Short description of required information or question that can be answered using the documentation

    Returns:
        str: Answer to the passed question
    """

    # Create instance of the class AzureCognitiveSearchRetriever
    retriever = AzureCognitiveSearchRetriever(
        content_key="content",
        service_name="hackathon-v2-ai-search",
        index_name="hackathon-v2-vector-idx-2",
        api_key=os.environ.get("AZURE_SEARCH_KEY"),
        top_k=10,
    )

    # Get the top_k most relevant chunks based on the question
    pass

    # Optional: Filter the retrieved documents based on a score-threshold (doc.metadata["@search.score"])
    pass

    # Build the new prompt that contains both the question as well as the relevant chunks
    pass

    # Create new ChatOpenAI instance to submit the new prompt
    pass

    # Invoke the new ChatOpenAI instance to retrieve the final answer based on the provided context
    pass

    return None


### BONUS: TOOL FOR VISUALIZING COLUMNS OF A TABLE (FROM THE DATABASE) ###


@tool
def visualize(table: str, column: str) -> str:
    """
    ### Description of the function
    ### IMPORTANT! The LLM decides to call it or not based on this docstring!

    Args:
        table (str): the table that holds the column that should be plotted
        column (str): the numerical column to plot

    Returns:
        str: the url in the backend that the visualization can be accessed with
    """

    # Create the URL to fetch the data from the correct endpoint
    pass

    # Fetch the data from the API using the URL
    pass

    # Plot the sedired column (using matplotlib)
    pass

    # Save the resulting figure on this webserver (in this case locally)
    pass

    # Return a response to the AI containing the markdown to display the image
    # --> Create a separate API endpoint for this
    return None
