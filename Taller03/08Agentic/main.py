from app.llm.openai_client import OpenAIClient
from app.services.agent_runner import AgentRunner
from app.schemas.tool_schemas import tools_schema
from app.tools.tool_registry import TOOL_REGISTRY
from app.agents.file_agent import get_initial_messages
import getpass

def main():
    print("Agent ready. Type 'exit' to stop.\n")

    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = getpass.getpass("Ingresa tu API Key de OpenAI : ")

    llm = OpenAIClient(api_key=api_key)
    agent = AgentRunner(llm, tools_schema, TOOL_REGISTRY)

    messages = get_initial_messages()

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        result = agent.run(messages, user_input)

        print("\nResult:")
        print(result)
        print("\n---\n")

if __name__ == "__main__":
    main()