import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_full_path, "r") as f:
            content = f.read(MAX_CHARS + 1)

        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS]
            return content + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        else:
            return content

    except UnicodeDecodeError:
        return f'Error: Could not read "{file_path}" as it is not a text file.'
    except PermissionError:
        return f'Error: Permission denied to read "{file_path}".'
    except Exception as e:
        return f'Error: An unexpected error occurred: {e}'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file up to a maximum number of characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read.",
            ),
        },
        required=["file_path"],
    ),
)