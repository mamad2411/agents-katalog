---
name: basic-agent-runner
description: Define an Agent and run it synchronously or asynchronously with Runner.
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, runner, async, agent-definition]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: examples/basic/hello_world.py
imported_at: 2026-04-18T00:00:00Z
---

# basic-agent-runner

Create a minimal `Agent` with instructions and run it with `Runner`. Use `Runner.run()` for async, `Runner.run_sync()` for synchronous, or `Runner.run_streamed()` for streaming.

## When to apply

Starting point for any agent integration using the OpenAI Agents SDK. Use when you need the simplest single-agent turn with a text reply.

## Core snippet

```python
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You only respond in haikus.",
)

async def main():
    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print(result.final_output)

asyncio.run(main())
```

## Variants

```python
# Synchronous (blocks)
result = Runner.run_sync(agent, "Hello!")
print(result.final_output)

# Streaming
result = Runner.run_streamed(agent, "Tell me 5 jokes.")
async for event in result.stream_events():
    # handle events
    pass
```

## Key properties

- `Agent(name, instructions)` — minimum required fields
- `result.final_output` — the text output of the last agent turn
- Default model is `gpt-4o`; override with `model="gpt-4o-mini"` on the `Agent`
- `Runner.run()` wraps a loop: model call → tool calls → model call until final output
