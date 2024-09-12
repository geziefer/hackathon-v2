# Hackathon v2 Backend: Python + OpenAI Functions

This is the backend for the second vSTI hackathon. It is based on OpenAI Functions and processes the incoming requests made by the frontend (React.js chat application) accordingly.


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

The value for the `OPENAI_API_KEY` will be provided by the organization.

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

The ask-assistant endpoint is the heart of the API, processing the incoming prompt through the OpenAI Completions API, equipped with functions for the model to choose from. When chatting with the system (posting prompts through the frontend), this endpoint gets invoked, it takes the prompt, processes it, and returns the result back to the user.

The clear-chat endpoint is a helper endpoint, that can be invoked to clear the chat history. Because we only want to develop a small showcase for the hackathon, no database for multiple chats was created. The conversation is stored in the Agent-instance instead.


## The "Agent" Class

This class is a wrapper for the OpenAI instance, that actually performs the calls to the OpenAI-API.

`So this can be seen as the Artificial Intelligence, that should be equipped with capabilities (tools).`

### __init__

Here all required attributes are set, which include
- self.messages: List of messages processed by the LLM, each following the schema {"role": \<system, user, assistant\>, "content": \<actual message\>}
- self.conversation: List of interactions between the bot and the user, very similar to `self.messages`, just in another format that is expected by the frontend
- self.client: The OpenAI instance to make calls to the OpenAI-API - the AI-instance itself
- self.tools: List of function-definitions in the format that the OpenAI API expects it to determine, which function to call to process the user's request. The passed object TOOLS is defined in the tools.py script.

### reset_messages

Resets the conversation history to start a new chat as well as the self.messages object to only contain the system prompt.

### get_response

Method to call when a prompt is submitted by the user. This method calls the OpenAI Completions API as well as handles the tools that should be invoked based on the user's query. The workflow looks as follows:

1. Call the OpenAI-Completions-API based on the user's prompt and the previous conversation
2. Check, if the model suggests to invoke a tool
3. Call the appropriate tool
4. Call the OpenAI-Completions-API again, together with the results returned by the tool
5. Return the final response

```text
IMPORTANT: This is where the tool-calls must be handled! When using OpenAI Functions, the tools do not get called automatically but have to be invoked manually instead. The model only suggests to call a tool!
This makes the development a little bit more complicated but also opens up new possibilities when invoking tools, that require special handling of the interim results.
```

## What is a "tool"?

When using the OpenAI-Functions Stub, a tool is nothing more than a function in Python. In contrast to the LangChain implementation (realized in the other stub), we do not bind the functions to the LLM directly and invoke a chain, that chooses a tool, calls it, and passes the results to a new LLM-call. Instead, OpenAI provides us the possibility to tell the model how the available functions look like, that includes the name, the arguments, and a description of the tool's purpose.

### Adding a new tool

In this example we want the model to greet a person on the console, so we start by defining the function.

```python
def greet_person(name: str) -> str:
    """
    OPTIONAL DOCSTRING
    """

    greeting = f"Hello {name}!"
    print(greeting)

    return greeting
```

After creating the function, we have to tell the model, that it exists. We do that by adding it to the `TOOLS` variable at the very top of the `tools.py` file. This variable is a list of dictionaries, each describing a single function (tool).

A single function definition (entry in the TOOLS-list) looks as follows.

```json
{
    "type": "function",
    "function": {
        "name": "greet_person",
        "description": "Greet a person specified by the name by printing the string 'Hello {name}!' on the console.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the person that should be greeted."
                }
            },
            "required": [],
        },
    },
},
```

If we take a look at the implementation of the Agent-class, the `TOOLS` object is being stored in the `self.tools` property of the instance. Later, when generating the response in the `get_response` method, the `self.tools` is passed to the completions-API call provided by the OpenAI-client.

### Handling the tool-invocation

The response made by OpenAI can include the `tool_calls` attribute, that, if present, states which tools should be invoked in order to properly handle the prompt that the user submitted in the first place.

In the case of a required tool, the invocation must be handled manually when using the native OpenAI completions API.

One example of a tool is already implemented.

```python
# Check, if the model wants to call a tool in order to process the user's prompt
tool_calls = resp_msg_obj.tool_calls
if tool_calls:
    # Iterate over the tools
    for tool_call in tool_calls:
        # A tool has been requested --> call it and process the result
        tool_call_id = tool_call.id
        tool_function_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        # Decide, which function to invoke
        # TODO: When adding more tools, the invocation must be handled here!
        if tool_function_name == "get_db_info":
            # Invoke the tool
            results = get_db_info(**tool_args)

            # Append the results returned by the tool-invocation to the messages list
            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": tool_function_name,
                    "content": str(results),
                }
            )

    # Call the model again with the new self.messages object
    # Provide the results to the agent
    # --> Answer the initial prompt based on the tools' results
    resp_with_function_call = self.client.chat.completions.create(
        model=config.GPT_VERSION,
        messages=self.messages,
        temperature=config.TEMPERATURE,
    )

    # Get the final result and append it to the self.messages object
    final_resp_msg = resp_with_function_call.choices[0].message.content
    self.messages.append({"role": "assistant", "content": final_resp_msg})
```

The section above implements how to handle a response, that might require a tool. The variable `resp_msg_obj` is retrieved from the OpenAI completions-API a few lines earlier and holds the information about potentially required usage of functions, that are defined in the `TOOLS` variable at the top of the file `tools.py`. After checking if the model wants to call a function by evaluating `tool_calls = resp_msg_obj.tool_calls` as a conditional, we have to handle the possibility of invoking more than one tool, so we iterate over `tool_calls`. Every single `tool_call` now holds an id, a function name, and arguments that need to be passed to that function and after retrieving that information we have to manually destinguish between the names of the functions that we equipped the agent with. So for example, when the `tool_function_name` evaluates to "get_db_info", we call the function `get_db_info` manually and pass the `**tool_args` as parameters. After retrieving the results, we append a new object to `self.messages` referencing the `tool_call_id`. This logic for that simple `get_db_info`-tool is being handled in the code block below.

```python
# Decide, which function to invoke
# TODO: When adding more tools, the invocation must be handled here!
if tool_function_name == "get_db_info":
    # Invoke the tool
    results = get_db_info(**tool_args)

    # Append the results returned by the tool-invocation to the messages list
    self.messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_function_name,
            "content": str(results),
        }
    )
```

```text
IMPORTANT: Those blocks have to be created for every tool that is being added during the hackathon!
```

After the `self.messages` object has been extended with the new information about the results returned by the invoked tool, the updated messages list must be passed to a new OpenAI completions-API call. OpenAI understands (and expects) every entry that references a required tool-request based on the `tool_call_id`. The retrieved results are now being processed by the LLM and the final answer is being generated.

That happens when calling the following code.

```python
# Call the model again with the new self.messages object
# Provide the results to the agent
# --> Answer the initial prompt based on the tools' results
resp_with_function_call = self.client.chat.completions.create(
    model=config.GPT_VERSION,
    messages=self.messages,
    temperature=config.TEMPERATURE,
)

# Get the final result and append it to the self.messages object
final_resp_msg = resp_with_function_call.choices[0].message.content
self.messages.append({"role": "assistant", "content": final_resp_msg})
```

The variable `final_resp_msg` is then being appended to self.conversation in order to render it in the frontend.
