from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import os
from llm import Provider


def main():
    provider = Provider(provider="anthropic", model="claude-3-5-sonnet-20241022")

    response = provider.get_response("Write a haiku about recursion in programming.")
    print(response)


if __name__ == "__main__":
    main()
