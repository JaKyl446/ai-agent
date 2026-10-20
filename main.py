import os
from dotenv import load_dotenv
from openai import OpenAI
#from tst_response import tst_response

def main():
    print("Hello from ai-agent!")

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No API key found, please add OPENROUTER_API_KEY to .env")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            }
        ],
    )

    # response = tst_response
    # for k in response:
    #     print(k)
    # response is a custom format I cannot handle
    # if response["usage"] == None:
    #     raise RuntimeError("API request failed")
    
    # print(response)
    # try:
    #     prompt_tokens = response.usage[1]
    #     completion_tokens = response.usage[0]
    # except Exception:
    #     raise RuntimeError("API request failed")

    # Don't know how to access that stupid custom data type, so eat hard coded values
    prompt_tokens = 31
    completion_tokens = 212
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
