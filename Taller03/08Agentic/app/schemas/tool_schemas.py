tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "create_text_file",
            "description": "Create empty text file",
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
            "description": "Write to CSV/TXT",
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
            "description": "Move file",
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
            "description": "Read file",
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