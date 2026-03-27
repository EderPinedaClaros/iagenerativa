from openai import OpenAI
from app.core.config import Settings

class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def chat(self, messages, tools):
        return self.client.chat.completions.create(
            model=Settings.MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )