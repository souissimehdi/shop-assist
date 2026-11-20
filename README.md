# ShopAssist

A support assistant for a fictional online store, built on Claude through Amazon Bedrock. Each script in
[`shopassist/`](shopassist/) shows one building block, from a single request to an agent with tools and subagents.

## Setup

```bash
cd shopassist
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                    # put your key in .env, never in the code
```

`.env` holds one line, `ANTHROPIC_API_KEY=...`, set to an **Amazon Bedrock API key** for `eu-west-2`. The scripts use
`AnthropicBedrock` with the model `eu.anthropic.claude-sonnet-5-5` (an EU inference profile). Bedrock short-term API keys
expire after 12 hours; put a fresh one in `.env` when you get authentication errors.

On current models a reply can start with a thinking block, so read the text from the text block rather than
`response.content[0]`.

## The scripts

| Script | What it shows | Run |
| --- | --- | --- |
| `first_request.py` | One `messages.create`, then `content`, `stop_reason` and `usage` | `python first_request.py` |
| `conversation.py` | The `messages` list is the only memory | `python conversation.py` |
| `app.py`, `static/index.html` | A chat UI in front of the script | `uvicorn app:app --port 8000`, open http://127.0.0.1:8000/ |
| `rules.py` | A prompt rule is a request, a code rule is a guarantee | `python rules.py` |
| `evaluate.py` | Two system prompts scored on the same test cases | `python evaluate.py` |
| `tool_call.py` | One tool call end to end: `tool_use`, run the function, send `tool_result` back | `python tool_call.py` |
| `extract.py` | Schema-valid output with `output_config.format` | `python extract.py` |
| `validate.py` | Business validation, then retry with the exact error, up to three attempts | `python validate.py` |
| `build_extract.py`, `emails/` | Five emails in, `return_requests.json` out | `python build_extract.py` |
| `agent_loop.py` | The agentic loop: repeat while `stop_reason == "tool_use"` | `python agent_loop.py` |
| `tool_errors.py` | Structured tool errors: `isError`, `errorCategory`, `isRetryable`, `customerMessage`, `developerMessage` | `python tool_errors.py` |
| `mcp_server.py` | The backend tools as an MCP server | `claude mcp add shopassist -- python mcp_server.py` |
| `agent.py` | A gate before the loop, a hook before every tool, escalation as a tool | `python agent.py` |
| `coordinator.py` | A coordinator calling two specialised agents as tools | `python coordinator.py` |
| `batch.py` | Message Batches API with `custom_id` and retries. Bedrock has no Batch API, so this one needs a first-party Anthropic API key | `python batch.py` |
| `CLAUDE.md`, `.claude/` | Claude Code project instructions, a rule and an `order-check` skill | `claude -p "Use the order-check skill for order ORD-87654321." --allowedTools "Skill,Bash(python *)"` |
| `ci_review.sh`, `review_schema.json` | Claude Code in CI with `-p` and JSON output | `sh ci_review.sh` |

The order IDs the tools know are `ORD-12345678` (a jacket, delivered 20 days ago) and `ORD-87654321` (a lamp, delivered 45 days ago).
Everything else returns `found: false`, which is data, not an error.

## The request trace

`shopassist/.trace/` is an optional observer. `sitecustomize.py` logs every HTTP exchange of the Anthropic client to `trace.jsonl`
when the folder is on `PYTHONPATH`; `trace.html` and `trace_mcp.html` draw it:

```bash
cd shopassist
export PYTHONPATH="$PWD/.trace"
(cd .trace && python3 -m http.server 8765 &)      # then open http://127.0.0.1:8765/trace.html
python first_request.py
```

## Credits

Based on the ShopAssist example project by termidy (https://github.com/termidy/CCAR-F-practice), which is free to use for
learning and in your own projects.
