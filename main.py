import os
from dotenv import load_dotenv
from openai import OpenAI
#from tst_response import tst_response
import argparse

def main():
    print("Hello from ai-agent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No API key found, please add OPENROUTER_API_KEY to .env")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "user", "content": args.user_prompt},
    ]
    
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    tokens = []
    try:
        tokens.append(response.usage[1])
        tokens.append(response.usage[0])
    except Exception:
        tokens.append("failed 1")
    try:
        tokens.append(response.usage.prompt_tokens)
        tokens.append(response.usage.completion_tokens)
    except Exception:
        tokens.append("failed 2")
    try:
        tokens.append(response.usage["prompt_tokens"])
        tokens.append(response.usage["completion_tokens"])
    except Exception:
        tokens.append("failed 3")
    try:
        tokens.append(response.choices[0].usage.prompt_tokens)
        tokens.append(response.choices[0].usage.completion_tokens)
    except Exception:
        tokens.append("failed 4")
    print(tokens)
    # Finally found the correct way to access the values
    try:
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
    except Exception:
        raise RuntimeError("API request failed")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {completion_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
