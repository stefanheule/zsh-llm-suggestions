#!/usr/bin/env python3

import sys
import os

MISSING_PREREQUISITES = "zsh-llm-suggestions missing prerequisites:"

def main():
    try:
        import openai
    except ImportError:
        print(f'echo "{MISSING_PREREQUISITES} Install OpenAI Python API." && pip3 install openai')
        return

    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key is None:
        print(f'echo "{MISSING_PREREQUISITES} OPENAI_API_KEY is not set." && export OPENAI_API_KEY="<copy from https://platform.openai.com/api-keys>"')
        return

    client = openai.Client(
        api_key=api_key,
    )

    buffer = sys.stdin.read()
    message=[
        {
            "role":'system',
            "content": """You are a zsh shell expert, please write a ZSH command that solves my problem.
    You should only output the completed command, no need to include any other explanation.""",
        },
        {"role": "user", "content": buffer}
    ]
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages = message,
        temperature=0.2,
        max_tokens=300,
        frequency_penalty=0.0
    )
    result = response.choices[0].message.content
    result = result.replace('```zsh', '').replace('```', '').strip()
    print(result)


if __name__ == '__main__':
    main()
