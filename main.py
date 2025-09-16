import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    available_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_args["working_directory"] = "./calculator"

    try:
        function_to_call = available_functions[function_name]
        function_result = function_to_call(**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error calling function: {e}"},
                )
            ],
        )

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='A command-line tool for asking a prompt.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'prompt',
        type=str,
        help='The prompt you want to ask. Enclose in quotes if it contains spaces.'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output.'
    )

    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = args.prompt

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if (args.verbose):
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")
    
    print("Response:")
    function_call_part = response.candidates[0].content.parts[0]

    if function_call_part.function_call:
        function_call_result = call_function(function_call_part.function_call, verbose=args.verbose)
        if not (function_call_result and
                function_call_result.parts and
                function_call_result.parts[0].function_response and
                function_call_result.parts[0].function_response.response):
            raise Exception("Unexpected function response structure.")

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print(response.text)

if __name__ == "__main__":
    main()
