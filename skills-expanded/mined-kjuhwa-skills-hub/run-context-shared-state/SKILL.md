---
name: run-context-shared-state
description: Pass typed shared state to all tools and hooks within an agent run via RunContextWrapper.
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, context, shared-state, dependency-injection]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: docs/context.md
imported_at: 2026-04-18T00:00:00Z
---

# run-context-shared-state

Create a typed context object (dataclass or Pydantic model) and pass it to `Runner.run(context=...)`. All tools, hooks, and lifecycle callbacks receive it via `RunContextWrapper[T].context`. The context is NOT sent to the LLM.

## When to apply

When tool functions need access to user data, database connections, loggers, or other runtime dependencies that should not appear in the model conversation.

## Core snippet

```python
import asyncio
from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo:
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Fetch the age of the user."""
    return f"The user {wrapper.context.name} is 47 years old"

async def main():
    user_info = UserInfo(name="John", uid=123)
    agent = Agent[UserInfo](
        name="Assistant",
        tools=[fetch_user_age],
    )
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )
    print(result.final_output)

asyncio.run(main())
```

## Key notes

- Context object is mutable; tools can write to it to share state across calls
- Every agent, tool, and hook in a run must use the same context type
- `RunContextWrapper` also exposes `.usage` (cumulative token counts) and `.approve_tool()`
- Context is not serialized into the conversation history; use it for ephemeral runtime state
