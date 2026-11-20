from dotenv import load_dotenv
import os
from anthropic import AnthropicBedrock

load_dotenv()
client = AnthropicBedrock(api_key=os.environ["ANTHROPIC_API_KEY"], aws_region="eu-west-2")

MODEL = "eu.anthropic.claude-sonnet-5-5"

CASES = [
    ("I bought a jacket, delivered 20 days ago. Can I return it?", "YES"),
    ("The shoes arrived yesterday. I want to send them back.", "YES"),
    ("My order was delivered 45 days ago. Can I still return it?", "NO"),
    ("I got a gift card last week. Can I return it?", "NO"),
    ("The underwear I ordered came 3 days ago. Return possible?", "NO"),
    ("Delivered 29 days ago, is a return still possible?", "YES"),
]

PROMPT_V1 = (
    "You are ShopAssist, an online store's support assistant. "
    "Returns are accepted within 30 days of delivery. "
    "Begin your answer with YES or NO, then one sentence."
)


def answer(system, text):
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,  # thinking counts toward this; 100 left no room for the answer
        output_config={"effort": "low"},
        system=system,
        messages=[{"role": "user", "content": text}],
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    return ""  # no text block: count it as a FAIL instead of crashing


def evaluate(name, system):
    score = 0
    for text, expected in CASES:
        reply = answer(system, text)
        ok = reply.strip().upper().startswith(expected)
        score += ok
        print("PASS" if ok else "FAIL", "|", text[:45], "|", reply[:40])
    print(name, "score:", score, "/", len(CASES))


evaluate("v1", PROMPT_V1)

PROMPT_V2 = PROMPT_V1 + (
    " Gift cards and underwear cannot be returned."
)
evaluate("v2", PROMPT_V2)
