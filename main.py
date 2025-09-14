import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

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

    # TODO: Remove when not being used
    # try:
    #     args = parser.parse_args()
    # except SystemExit:
    #     sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    ususer_prompt = args.prompt

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=ususer_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if (args.verbose):
        print("User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")
    
    print("Response:")
    function_call_part = response.candidates[0].content.parts[0]
    if function_call_part.function_call:
        print(f"Calling function: {function_call_part.function_call.name}({function_call_part.function_call.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
