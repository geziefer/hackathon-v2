from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

import config
from tools import TOOLS, get_db_info

import json


load_dotenv(find_dotenv(), override=True)


class Agent:
    def __init__(self) -> None:
        self.messages = [{"role": "system", "content": config.SYSTEM_PROMPT}]
        # Separate conversation object to display in frontend
        self.conversation = []
        self.client = OpenAI()
        self.tools = TOOLS

    def reset_messages(self) -> None:
        self.messages = [{"role": "system", "content": config.SYSTEM_PROMPT}]
        self.conversation = []

    def get_response(self, prompt: str) -> str:
        # Create the timestamp part for the prompt to enable queries relative to real time
        timestamp_prompt_part = (
            f"\n\nTimestamp: {datetime.now().strftime(config.DATETIME_FORMAT)}"
        )

        # Add user's prompt to the messages object of the Agent-instance
        self.messages.append(
            {"role": "user", "content": prompt + timestamp_prompt_part}
        )

        # Call the OpenAI-Completions-API, pass tools to the API-call
        chat_resp = self.client.chat.completions.create(
            model=config.GPT_VERSION,
            messages=self.messages,
            tools=self.tools,
            tool_choice=None,
        )
        resp_msg_obj = chat_resp.choices[0].message
        final_resp_msg = resp_msg_obj.content

        # Extend the self.messages object by the response of the LLM
        self.messages.append(resp_msg_obj)

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

        # Only append the initial prompt together with the final result to the
        # self.conversation object to be rendered in the frontend
        self.conversation.append({"user": prompt, "bot": final_resp_msg})

        return final_resp_msg
