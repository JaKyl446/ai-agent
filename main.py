import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_LOOPS


def main():
    print("Hello from ai-agent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No API key found, please add OPENROUTER_API_KEY to .env")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    prompt_tokens, completion_tokens = None, None
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(MAX_LOOPS):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        try:
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
        except Exception:
            raise RuntimeError("API request failed")
        if args.verbose:
            print(f"System prompt: {system_prompt}")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls != None:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                if not result_message["content"]:
                    raise Exception("received no content from call_function")
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(message.content)
            return

    print(f"Loop limit ({MAX_LOOPS}) reached. Aborting...")
    sys.exit(1)


if __name__ == "__main__":
    main()
