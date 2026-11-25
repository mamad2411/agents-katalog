---
name: streaming-agent-response
description: Stream agent output token-by-token or item-by-item using Runner.run_streamed().
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, streaming, sse, run-streamed]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: examples/basic/stream_text.py
imported_at: 2026-04-18T00:00:00Z
---

# streaming-agent-response

Use `Runner.run_streamed()` to get a `RunResultStreaming` object. Iterate `result.stream_events()` to receive raw token deltas or higher-level run items as they arrive.

## When to apply

Chat UIs needing progressive text display, long-running agents where the user should see progress, or any scenario where latency-to-first-token matters.

## Token-level streaming

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

async def main():
    agent = Agent(name="Joker", instructions="You are a helpful assistant.")
    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

asyncio.run(main())
```

## Item-level streaming

```python
from agents import Agent, ItemHelpers, Runner

async def main():
    agent = Agent(name="Joker", instructions="First call how_many_jokes, then tell jokes.", tools=[...])
    result = Runner.run_streamed(agent, input="Hello")
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print(f"Tool called: {event.item.raw_item.name}")
            elif event.item.type == "message_output_item":
                print(f"Message: {ItemHelpers.text_message_output(event.item)}")
```

## Key notes

- Always drain `stream_events()` to completion; the run is not complete until the iterator ends
- `RunResultStreaming.interruptions` is populated after the stream ends if tool approval is needed
- Call `result.cancel(mode="after_turn")` to stop cleanly after the current turn
- `result.is_complete` reflects final run state only after the iterator finishes
