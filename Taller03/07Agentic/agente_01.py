import os
import shutil
import json
import pandas as pd
from openai import OpenAI
import getpass

# ==============================
# 🔐 OPENAI CLIENT
# ==============================
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = getpass.getpass("Ingresa tu API Key de OpenAI : ")
)

# ==============================
# 🛠️ TOOLS (MISMA LÓGICA)
# ==============================

def move_file(source: str, destination_folder: str) -> str:
    try:
        if not os.path.exists(source):
            return f"Error: Source file '{source}' does not exist."

        if not os.path.exists(destination_folder):
            return f"Error: Destination folder '{destination_folder}' does not exist."

        filename = os.path.basename(source)
        destination_path = os.path.join(destination_folder, filename)

        shutil.move(source, destination_path)

        return f"Successfully moved {source} to {destination_path}"

    except Exception as e:
        return f"Move failed: {str(e)}"


def write_file(file_path: str, name: str, value: int) -> str:
    try:
        if not file_path or not file_path.strip():
            return "Error: File path cannot be empty."

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in [".csv", ".txt"]:
            return "Error: Only .csv or .txt files are allowed."

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
            except pd.errors.EmptyDataError:
                df = pd.DataFrame(columns=["Name", "Value"])
        else:
            df = pd.DataFrame(columns=["Name", "Value"])

        new_row = {"Name": [name], "Value": [value]}
        df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)

        df.to_csv(file_path, index=False, encoding="utf-8")

        return f"Success: Added {name} with value {value} to {file_path}"

    except Exception as e:
        return f"Failed to update file '{file_path}': {str(e)}"


def read_text_file(filename: str) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def create_text_file(filename: str) -> str:
    try:
        if not filename or not filename.strip():
            return "Error: Filename cannot be empty."

        if os.path.isabs(filename) or ".." in filename:
            return "Error: Only simple filenames are allowed (no paths)."

        with open(filename, "x", encoding="utf-8"):
            pass

        return f"Successfully created empty file '{filename}'."

    except FileExistsError:
        return f"Error: File '{filename}' already exists."
    except Exception as e:
        return f"File creation failed: {str(e)}"


# ==============================
# 🔧 TOOL DEFINITIONS (OPENAI)
# ==============================
# properties type: "string" | "integer" | "number" | "boolean" | "array" | "object"
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_text_file",
            "description": "Creates an empty text file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Insert row into CSV or TXT",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "name": {"type": "string"},
                    "value": {"type": "integer"}
                },
                "required": ["file_path", "name", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_file",
            "description": "Move file to folder",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "destination_folder": {"type": "string"}
                },
                "required": ["source", "destination_folder"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_text_file",
            "description": "Read file content",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"}
                },
                "required": ["filename"]
            }
        }
    }
]

# ==============================
# 🧠 TOOL MAP
# ==============================
tool_map = {
    "move_file": move_file,
    "write_file": write_file,
    "create_text_file": create_text_file,
    "read_text_file": read_text_file
}


# ==============================
# 🤖 SYSTEM PROMPT
# ==============================
system_prompt = """
You are a strict file management agent. IMPORTANT:

- You MUST ONLY use the provided tools:
- create_text_file(filename)
- write_file(file_path, name, value)
- move_file(source, destination_folder)
- read_text_file(filename)
- You MUST NOT write Python code
- You MUST NOT simulate file operations
- ALWAYS call tools
- After a successful tool call, STOP immediately
"""

# ==============================
# 🚀 AGENT LOOP
# ==============================
if __name__ == "__main__":
    print("Agent ready. Type 'exit' or 'quit' to stop.\n")

    messages = [{"role": "system", "content": system_prompt}]

    while True:
        user_prompt = input("What would you like the agent to do?\n> ")

        if user_prompt.lower() in ["exit", "quit"]:
            print("Stopping agent...")
            break

        if not user_prompt.strip():
            print("Please enter a valid instruction.\n")
            continue

        messages.append({"role": "user", "content": user_prompt})

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                verbosity="medium"
            )

            msg = response.choices[0].message

            if msg.tool_calls:
                tool_call = msg.tool_calls[0]
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if function_name not in tool_map:
                    raise Exception(f"Tool '{function_name}' no permitida")

                result = tool_map[function_name](**arguments)

                messages.append(msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

                print("\nResult:")
                print(result)
                print("\n---\n")

            else:
                print(msg.content)

        except Exception as e:
            print(f"Error: {e}\n")