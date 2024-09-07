from openai import OpenAI
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config.env")

# Get API Key from environment variable OPENROUTER_API_KEY
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=getenv("OPENROUTER_API_KEY"),
)


# Create a completion request
completion = client.chat.completions.create(
    model="google/gemini-flash-8b-1.5-exp",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is the image about?"},
                {
                    "type": "image_url",
                    "image_url": {"url": "https://i.imgur.com/Yi3hL5c.jpeg"},
                },
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Give a brief description of the colors in the image.",
                }
            ],
        },
    ],
)


# print(completion)
print(completion.choices[0].message.content)
# Save the entire response
with open("response.json", "w") as f:
    f.write(completion.json())
    print("Response saved to response.json")
