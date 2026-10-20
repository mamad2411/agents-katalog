# Anthropic SDK (Python) — Reference Guide

Official Python SDK for the Anthropic API. Full-featured client for Claude models — Messages, Batches, Files, Skills, and the Beta platform (Managed Agents, Sessions, Dreams, MemoryStores, Vaults, and more).

**Source:** `anthropics/anthropic-sdk-python` (public)
**Local clone:** `/home/user/anthropics/anthropic-sdk-python`
**Docs:** https://platform.claude.com/docs/en/api/sdks/python
**API reference:** `/home/user/anthropics/anthropic-sdk-python/api.md`
**Requires:** Python 3.10+

---

## Installation

```bash
pip install anthropic
```

---

## Basic Usage

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")  # or reads ANTHROPIC_API_KEY env var

message = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}],
)
print(message.content[0].text)
```

### Async client

```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic()
message = await client.messages.create(...)
```

---

## API Namespaces

### Messages — `client.messages`

Core inference. Supports text, images, PDFs, tool use, extended thinking, citations, computer use, and streaming.

```python
# Basic
msg = client.messages.create(model=..., max_tokens=..., messages=[...])

# Token count
count = client.messages.count_tokens(model=..., messages=[...])

# Streaming (see Streaming section)
with client.messages.stream(...) as stream: ...
```

### Batches — `client.messages.batches`

Asynchronous bulk inference; lower cost and higher throughput.

```python
batch = client.messages.batches.create(requests=[...])
batch = client.messages.batches.retrieve(batch_id)
batches = client.messages.batches.list()
results = client.messages.batches.results(batch_id)  # JSONL stream
client.messages.batches.cancel(batch_id)
client.messages.batches.delete(batch_id)
```

### Models — `client.models`

```python
model_info = client.models.retrieve("claude-opus-5")
models = client.models.list()  # SyncPage[ModelInfo]
```

### Files — `client.files`

Upload, download, and manage files (PDFs, images, data) for use in messages.

```python
meta = client.files.upload(file=open("doc.pdf", "rb"))
meta = client.files.retrieve_metadata(file_id)
files = client.files.list()
content = client.files.download(file_id)   # BinaryAPIResponse
client.files.delete(file_id)
```

### Skills — `client.skills`

Manage Claude Code skills programmatically.

```python
skill = client.skills.create(...)
skill = client.skills.retrieve(skill_id)
skills = client.skills.list()
client.skills.delete(skill_id)

# Versions
ver = client.skills.versions.create(skill_id, ...)
ver = client.skills.versions.retrieve(version, skill_id=skill_id)
client.skills.versions.list(skill_id)
client.skills.versions.delete(version, skill_id=skill_id)
```

---

## Beta APIs — `client.beta`

### Beta Messages — `client.beta.messages`

Extended message features: tool use, computer use, code execution, browser use, compaction, citations.

```python
msg = client.beta.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    tools=[...],
    messages=[...],
    betas=["computer-use-2025-10-01"],
)
```

#### Tool runner (agentic loop)

```python
runner = client.beta.messages.tool_runner(
    model="claude-sonnet-5",
    max_tokens=1024,
    tools=[my_tool],
    messages=[{"role": "user", "content": "..."}],
)
for message in runner:   # iterates: tool_use → call tools → send results → final message
    print(message)
```

### Managed Agents — `client.beta.agents`

Server-hosted agent execution environment with sandboxed tools.

```python
agent = client.beta.agents.create(...)
agent = client.beta.agents.retrieve(agent_id)
client.beta.agents.list()
client.beta.agents.delete(agent_id)
```

### Environments — `client.beta.environments`

Sandbox environments for agent tool execution.

```python
env = client.beta.environments.create(...)
env = client.beta.environments.retrieve(env_id)
envs = client.beta.environments.list()
client.beta.environments.delete(env_id)
```

### Sessions — `client.beta.sessions`

Persistent agent sessions. Core of the Managed Agents API.

```python
# Session lifecycle
session = client.beta.sessions.create(agent_id=..., ...)
msg = client.beta.sessions.messages.create(session_id, messages=[...])
events = client.beta.sessions.events.list(session_id)    # stream events
client.beta.sessions.delete(session_id)
```

### Deployments — `client.beta.deployments`

Package and version agents for production deployment.

```python
dep = client.beta.deployments.create(...)
run = client.beta.deployment_runs.create(deployment_id=..., ...)
run = client.beta.deployment_runs.retrieve(run_id)
```

### Vaults — `client.beta.vaults`

Secure credential storage for agent tool access (egress proxy substitutes token at request time).

```python
vault = client.beta.vaults.create(name=..., ...)
vaults = client.beta.vaults.list()
client.beta.vaults.delete(vault_id)

# Secrets within a vault
secret = client.beta.vaults.secrets.create(vault_id, ...)
client.beta.vaults.secrets.list(vault_id)
client.beta.vaults.secrets.delete(vault_id, secret_id)
```

### Memory Stores — `client.beta.memory_stores`

Versioned knowledge bases for agents.

```python
store = client.beta.memory_stores.create(...)
store = client.beta.memory_stores.retrieve(store_id)
client.beta.memory_stores.list()
client.beta.memory_stores.delete(store_id)

# Documents in a store
client.beta.memory_stores.documents.create(store_id, ...)
client.beta.memory_stores.documents.list(store_id)
client.beta.memory_stores.documents.delete(store_id, doc_id)
```

### Dreams — `client.beta.dreams`

Consolidation / background synthesis jobs. Used for knowledge distillation and wiki-building patterns.

```python
dream = client.beta.dreams.create(...)
dream = client.beta.dreams.retrieve(dream_id)
dreams = client.beta.dreams.list()
```

### Webhooks — `client.beta.webhooks`

Register endpoints to receive `session.status_idled` and other events.

```python
wh = client.beta.webhooks.create(url=..., events=[...])
wh = client.beta.webhooks.retrieve(webhook_id)
client.beta.webhooks.list()
client.beta.webhooks.delete(webhook_id)
```

### User Profiles — `client.beta.user_profiles`

Per-user context and preferences.

```python
profile = client.beta.user_profiles.retrieve(user_id)
client.beta.user_profiles.update(user_id, ...)
```

### Tunnels — `client.beta.tunnels`

Expose local servers for agent sandbox access.

### Organization — `client.beta.organization`

Manage org-level settings, members, and API keys.

---

## Streaming

### Text streaming (simplest)

```python
with client.messages.stream(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

final = stream.get_final_message()
```

### Event streaming

```python
async with client.messages.stream(...) as stream:
    async for event in stream:
        if event.type == "text":
            print(event.text)          # delta
            print(event.snapshot)      # accumulated so far
        elif event.type == "input_json":
            print(event.partial_json)
        elif event.type == "content_block_stop":
            print(event.content_block)
        elif event.type == "message_stop":
            print(event.message)
```

### Raw stream (lower memory)

```python
with client.messages.create(..., stream=True) as stream:
    for event in stream:
        ...
```

---

## Tool Use

### Decorator approach (`@beta_tool`)

```python
from anthropic import beta_tool

@beta_tool
def get_weather(location: str) -> str:
    """Get current weather for a location.
    Args:
        location (str): City and country, e.g. 'Athens, GR'.
    Returns:
        str: Weather description.
    """
    return f"Sunny, 28°C in {location}"

# Pass to API — schema auto-generated from docstring + type hints
msg = client.beta.messages.create(
    tools=[get_weather],
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What's the weather in Athens?"}],
)
```

For async functions use `@beta_async_tool`.

### Manual tool definition

```python
tools = [{
    "name": "get_weather",
    "description": "Get weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {"location": {"type": "string"}},
        "required": ["location"],
    },
}]
```

---

## Extended Thinking

```python
msg = client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "Solve step by step: ..."}],
)
for block in msg.content:
    if block.type == "thinking":
        print(block.thinking)   # CoT
    elif block.type == "text":
        print(block.text)
```

---

## Prompt Caching

Add `cache_control` to stable content to reduce latency and cost on repeated calls:

```python
client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": "Very long stable system prompt...",
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{"role": "user", "content": "Short user turn"}],
)
```

---

## Computer Use

```python
msg = client.beta.messages.create(
    model="claude-sonnet-5",
    max_tokens=4096,
    tools=[{"type": "computer_20260801", "name": "computer"}],
    messages=[{"role": "user", "content": "Take a screenshot"}],
    betas=["computer-use-2026-08-01"],
)
```

Computer action types: `screenshot`, `left_click`, `right_click`, `double_click`, `type`, `key`, `scroll`, `mouse_move`, `hold_key`.

---

## Examples (in `/home/user/anthropics/anthropic-sdk-python/examples/`)

| File | What it shows |
|------|--------------|
| `messages.py` | Basic message creation |
| `messages_stream.py` | Streaming with helpers |
| `tools.py` | Tool use (manual) |
| `tools_runner.py` | Tool runner / agentic loop |
| `tools_runner_search_tool.py` | Search tool with runner |
| `tools_stream.py` | Streaming + tool calls |
| `thinking.py` | Extended thinking (non-streaming) |
| `thinking_stream.py` | Extended thinking (streaming) |
| `structured_outputs.py` | Structured JSON outputs |
| `structured_outputs_streaming.py` | Structured outputs + streaming |
| `agents.py` | Managed Agents basic example |
| `agents_comprehensive.py` | Full Managed Agents patterns |
| `agents_with_files.py` | Agents + Files API |
| `managed-agents-streaming-deltas-manual.py` | Streaming event deltas manually |
| `managed-agents-worker-dispatch.py` | Worker dispatch pattern |
| `web_search.py` | Web search tool |
| `images.py` | Image input |
| `batch_results.py` | Message Batches |
| `mcp_tool_runner.py` | MCP tool runner |
| `memory/` | Memory store patterns |

---

## Prompts

### Implement a tool-calling agent

```
Using /home/user/anthropics/anthropic-sdk-python/examples/tools_runner.py as reference:
Build a [use-case] agent using client.beta.messages.tool_runner() with these tools: [list].
```

### Build a Managed Agents integration

```
Using /home/user/anthropics/anthropic-sdk-python/examples/agents_comprehensive.py:
Implement a [Slack/webhook/scheduled] integration using the Sessions API.
Key requirements: [list them].
```

### Stream extended thinking

```
Using /home/user/anthropics/anthropic-sdk-python:
Write a streaming extended thinking example for [task].
Show both the thinking blocks and the final answer.
```

### Batch processing

```
Using client.messages.batches from anthropic-sdk-python:
Write a batch job that processes [N] [items] and streams results as they complete.
```
