from dotenv import load_dotenv
import os
from anthropic import AnthropicBedrock

load_dotenv()
client = AnthropicBedrock(api_key=os.environ["ANTHROPIC_API_KEY"], aws_region="eu-west-2")

MODEL = "eu.anthropic.claude-sonnet-5-5"
SYSTEM = (
    "You are ShopAssist, an online store's support assistant. "
    "Returns are accepted within 30 days of delivery. "
    "Answer in one or two sentences."
)


def ask(messages):
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        output_config={"effort": "low"},
        system=SYSTEM,
        messages=messages,
    )
    for block in response.content:
        if block.type == "text":
            reply = block.text
    print(reply)
    print("input tokens:", response.usage.input_tokens)
    return reply


history = []


def say(text):
    history.append({"role": "user", "content": text})
    reply = ask(history)
    history.append({"role": "assistant", "content": reply})


say("I bought a jacket 20 days ago.")
say("Can I still return it?")
say("And if I lost the receipt?")
