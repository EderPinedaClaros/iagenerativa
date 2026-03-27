import os
import shutil
import pandas as pd

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
        return f"Failed: {str(e)}"


def read_text_file(filename: str) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"


def create_text_file(filename: str) -> str:
    try:
        if os.path.isabs(filename) or ".." in filename:
            return "Error: Invalid filename."

        with open(filename, "x", encoding="utf-8"):
            pass

        return f"Created file '{filename}'"

    except FileExistsError:
        return f"Error: File exists."