import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the text content of a specific file. The tool enforces security by restricting access to the working directory and truncates output if the file exceeds the character limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file that needs to be read (e.g., 'src/main.py' or 'notes.txt').",
            ),
        },
        required=["file_path"]
    ),
)


def get_file_content(working_directory, file_path):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
            
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path

        if not valid_target_file:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            
        if not os.path.isfile(target_file):
                return f'Error: "File not found or is not a regular file: "{file_path}"'
        
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content

    except Exception as e:
        return f"Error listing files: {e}"