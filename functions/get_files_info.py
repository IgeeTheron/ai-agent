import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(abs_full_path):
            return f'Error: The directory "{directory}" was not found.'

        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'

        items = os.listdir(abs_full_path)
        output_lines = []

        for item in items:
            item_path = os.path.join(abs_full_path, item)
            is_dir = os.path.isdir(item_path)

            try:
                file_size = os.path.getsize(item_path)
            except Exception:
                file_size = -1

            line = f'- {item}: file_size={file_size} bytes, is_dir={is_dir}'
            output_lines.append(line)

        return "\n".join(output_lines)


    except FileNotFoundError:
        return f'Error: The directory "{directory}" was not found.'
    except PermissionError:
        return f'Error: Permission denied to access "{directory}".'
    except Exception as e:
        return f'Error: An unexpected error occurred: {e}'
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
