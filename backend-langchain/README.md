# Hackathon v2 Backend: Python + LangChain

This is the backend for the second vSTI hackathon. It is based on LangChain Agents and processes the incoming requests made by the frontend (React.js chat application) accordingly.


## Setup

In general it is recommended to create a virtual environment for Python to encapsulate all dependencies used in this project from your global Python installation.
To do this, run the following command.

```bash
python -m venv venv
```

This creates a directory `venv` in your current working directory (you can adapt the name of the environment by changing the second `venv` in the command mentioned above).
After that, activate the environment by executing

```bash
.\venv\Scripts\activate
```

on Windows- or

```bash
source venv/bin/activate
```

on Unix-Systems.

After successfully activating the environment, the name should be displayed in brackets at the very start of your command line, like e.g. `(venv)`.

To run the API, you need to execute two steps.

1. Install all modules from the requirements.txt file

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the field

```text
OPENAI_API_KEY="..."
```

The value for the `OPENAI_API_KEY` will be provided by vSTI.

After that, you can simply start the application by calling

```bash
python server.py
```

on Windows- and

```bash
python3 server.py
```

on Unix-Systems.

## How it works

The base is a Flask API that exposes only 2 endpoints

1. ask-assistant
2. clear-chat

The ask-assistant endpoint is the heart of the API, processing the incoming prompt through the Agent-instance (explained in the next section). When chatting with the system (posting prompts through the frontend), this endpoint gets invoked, it takes the prompt, processes it (agent), and returns the result back to the user.

The clear-chat endpoint is a helper endpoint, that can be invoked to clear the chat history. Because we only want to develop a small showcase for the hackathon, no database for multiple chats was created. The current conversation is stored in the Agent-instance instead.


## The "Agent" Class

This class is a wrapper for the ChatOpenAI instance, that actually performs the calls to the OpenAI-API.

`So this can be seen as the Artificial Intelligence, that should be equipped with capabilities (tools).`

### __init__

Here all required attributes are set, which include
- llm: ChatOpenAI instance, that makes calls to the OpenAI-API
- tools: list of functions that the Agent can invoke that can help the llm respond to the user's prompt (call APIs, search in documentation, etc.)
- prompt: ChatPromptTemplate to pass all required information to the agent when invoking it
- agent: instance choosing an appropriate tool and processing the prompt based on the passed llm
- self.agent_executor: combines the agent and the tools to respond to the user's query
- self.conversation: list of interactions between the user and the agent, each consisting of a user's prompt and an agent's response

### reset_messages

Resets the conversation history to start a new chat.

### create_chat_history

Creates a chat history in the format that LangChain expects it, using HumanMessage- and AIMessage-instances. The self.conversation attribute serves as a base for this.

### get_response

Method to call when a prompt is submitted by the user. This method calls `create_chat_history`, invokes the agent executor chain, and extends the self.conversation attribute of the "Agent" instance, to provide memory.


## What is a "tool"?

A tool is a function that the agent can invoke to either get more information to respond to the user's query or to perform an action the user asked for. The arguments of the invoked tool are populated by the LLM itself.

### LangChain structure for tools

With LangChain, every tool needs to be annotated with the `@tool` annotaion, which is already imported at the top of the file.

```python
from langchain.agents import tool
```

After importing the required annotation like shown above, the function that the agent should be equipped with can be created.

```python
@tool
def greet_person(name: str) -> str:
    """
    This function can be used to greet a person specified by the name.
    It prints out "Hello {name}!" on the console.

    Args:
        name (str): Name of the person that should be greeted.

    Returns:
        str: Greeting, that was printed out on the console.
    """

    # Print out the greeting --> perform the actual logic of the function
    # This can be custom logic, API calls, Database-Queries, ...
    greeting = f"Hello {name}!"
    print(greeting)

    return greeting
```

```text
IMPORTANT: The Docstring is required and must be "well-written".
The LLM reads it and decides based on that if it should invoke the tool or not!
```

After the tool has been created, equipped with a well engineered docstring, it can be bound to the Agent-class. To do that, go to the `Agent.py` file and in the `__init__` method, look for the variable `tools`, that is a list of functions. To add the newly created tool `greet_person` you have to import it at the top of the file first.

```python
from tools import get_db_info, greet_person
```

After importing it, simply add it to the list in the `__init__` method

```python
# Define the List of Tools, that the Agent should have Access to
tools = [get_db_info, greet_person]
```

The result returned by the tool is handled by LangChain automatically, it gets passed to a new LLM-call that produces the final result.
No further adaptions have to be made in this stub, when prompting the chatbot to greet a person by a name, the agent will automatically invoke the tool.
