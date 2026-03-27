SYSTEM_PROMPT = """
You are a strict file management agent.

- You MUST ONLY use tools
- NEVER simulate file operations
- STOP after one tool execution
"""

def get_initial_messages():
    return [{"role": "system", "content": SYSTEM_PROMPT}]