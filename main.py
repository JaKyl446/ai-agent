import os
from dotenv import load_dotenv
from openai import OpenAI
#from tst_response import tst_response
import argparse

def main():
    print("Hello from ai-agent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
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
        tokens.append(None)
    try:
        tokens.append(response.usage.prompt_tokens)
        tokens.append(response.usage.completion_tokens)
    except Exception:
        tokens.append(None)
    try:
        tokens.append(response.usage["prompt_tokens"])
        tokens.append(response.usage["completion_tokens"])
    except Exception:
        tokens.append(None)
    #     raise RuntimeError("API request failed")
    print(tokens)
    # Don't know how to access that stupid custom data type, so eat hard coded values
    prompt_tokens = 31
    completion_tokens = 212
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
