import os

from dotenv import load_dotenv
from anthropic import AnthropicBedrock

load_dotenv()
# The Bedrock API key sits in ANTHROPIC_API_KEY in .env; region matches the key (eu-west-2).
# Mantle (AnthropicBedrockMantle) 404s every model on this account, so use bedrock-runtime.
client = AnthropicBedrock(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    aws_region="eu-west-2",
)

# Bedrock needs an inference profile ID for on-demand use (eu.* keeps traffic in the EU).
MODEL = "eu.anthropic.claude-sonnet-5-5"

response = client.messages.create(
    model=MODEL,
    max_tokens=300,
    output_config={"effort": "low"},
    messages=[{
        "role": "user",
        "content": "A customer asks: can I return "
        "a jacket after 20 days? Our policy allows "
        "returns within 30 days. Answer the customer "
        "in two sentences.",
    }],
)

print(response.content[0].text)
print("stop_reason:", response.stop_reason)
print("usage:", response.usage.input_tokens,
      response.usage.output_tokens)
