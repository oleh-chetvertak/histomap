import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
API_CHAT_GPT = os.getenv("API_CHAT_GPT")
client = OpenAI(api_key=API_CHAT_GPT)


def RequestGPT(model, role, content):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": role, "content": content}],
    )
    return completion
