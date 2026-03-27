import json
from app.core.logger import logger

class AgentRunner:

    def __init__(self, llm_client, tools_schema, tool_registry):
        self.llm = llm_client
        self.tools = tools_schema
        self.tool_registry = tool_registry

    def run(self, messages, user_input):

        messages.append({"role": "user", "content": user_input})

        response = self.llm.chat(messages, self.tools)
        msg = response.choices[0].message

        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            logger.info(f"Tool call: {function_name} | Args: {arguments}")

            if function_name not in self.tool_registry:
                raise Exception(f"Tool '{function_name}' not allowed")

            result = self.tool_registry[function_name](**arguments)

            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

            return result

        return msg.content