from typing import List, Dict
import config
import os
from langchain_community.retrievers import AzureCognitiveSearchRetriever


### EXAMPLE OF TOOLS WITH PARAMETERS --> CHANGE PROPERTIES ATTRIBUTE OF FUNCTION DEFINITION ###
#  "properties": {
#      "production_line_number": {
#          "type": "integer",
#          "enum": [1, 2],
#          "description": "The number of the production line.",
#      },
#  },


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_db_info",
            "description": "Get information about the available database, it's tables and their respective columns.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


def get_db_info() -> str:
    """
    This function can be used to retrieve information about the database, that can be accessed.
    It returns a text describing the database's structure for the user.

    Returns:
        str: text, describing the database-structure
    """
    print("Getting DB Info...")

    return config.DATABASE_DESCR


### TASK 1: GET IIOT DATA (input, ambient, machine, qa) ###


def get_machine_data(
    from_timestamp: str | None,
    to_timestamp: str | None,
) -> List[float]:
    # Prepare the URL to call the Factory's API (Note: use config.BACKEND_URL)
    pass

    # Send the request to get the data from the machine endpoint
    pass

    # Optional: Postprocess the data to be in your desired format
    pass

    return []


# Question: Do you need to invoke the API Endpoints for the other tables as well? (input, ambient, qa)


### TASK 2: QUERY LOGS-API-ENDPOINT ###


def get_logs(
    from_timestamp: str | None, to_timestamp: str | None
) -> List[Dict[str, str]]:
    # Prepare the URL to call the Factory's API
    pass

    # Send the request to get the data from the logs endpoint
    pass

    # Optional: Postprocess the data to be in your desired format
    pass

    return []


### TASK 3: QUERY DOCUMENTATION USING RAG ###


def query_documentation(question: str) -> str:
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


def visualize(table: str, column: str) -> str:
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
