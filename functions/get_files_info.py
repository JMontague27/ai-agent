import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        results = []
        
        for name in sorted(os.listdir(target_dir)):
            item_path = os.path.join(target_dir, name)
            
            # Get metadata
            stats = os.stat(item_path)
            is_dir = os.path.isdir(item_path)
            file_size = stats.st_size
            
            # 3. Format the string as requested
            results.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")
        
        # Return the list of strings joined by newlines
        return "\n".join(results)
    except Exception as e:
        return f"Error listing files: {e}"
    

   