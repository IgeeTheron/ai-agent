import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    messages = [
        types.Content(role="user", parts=[types.Part(text=ususer_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if (args.verbose):
        print("User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")
    
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
