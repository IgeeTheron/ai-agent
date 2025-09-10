import os
import argparse
from dotenv import load_dotenv
from google import genai

def main():
    parser = argparse.ArgumentParser(
        description='A command-line tool for asking a prompt.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'prompt',
        type=str,
        help='The prompt you want to ask. Enclose in quotes if it contains spaces.'
    )

    args = parser.parse_args()

    # TODO: Remove when not being used
    # try:
    #     args = parser.parse_args()
    # except SystemExit:
    #     sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=args.prompt)

    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count }")


if __name__ == "__main__":
    main()
