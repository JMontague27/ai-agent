import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates a new file or overwrites an existing one with the provided content. It automatically creates any missing parent directories. Use this to save code, logs, or documentation.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path where the file should be saved (e.g., 'outputs/result.json' or 'new_script.py').",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The full text content to be written to the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
            
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path

        if not valid_target_file:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
        if os.path.isdir(target_file):
                return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing content: {e}"