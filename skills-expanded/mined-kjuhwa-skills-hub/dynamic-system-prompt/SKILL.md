---
name: dynamic-system-prompt
description: Generate agent instructions dynamically at runtime from a context object.
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, instructions, dynamic-prompt, context]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: examples/basic/dynamic_system_prompt.py
imported_at: 2026-04-18T00:00:00Z
---

# dynamic-system-prompt

Pass a callable to `Agent.instructions` instead of a static string. The callable receives `RunContextWrapper[TContext]` and the agent, returns a `str`. This enables per-user or per-request instruction customization.

## When to apply

When the agent's system prompt depends on runtime data (user role, session config, locale, A/B flags). Avoids maintaining multiple agent instances for minor prompt variants.

## Core snippet

```python
from dataclasses import dataclass
from typing import Literal
from agents import Agent, RunContextWrapper, Runner

@dataclass
class CustomContext:
    style: Literal["haiku", "pirate", "robot"]

def custom_instructions(
    run_context: RunContextWrapper[CustomContext], agent: Agent[CustomContext]
) -> str:
    context = run_context.context
    if context.style == "haiku":
        return "Only respond in haikus."
    elif context.style == "pirate":
        return "Respond as a pirate."
    else:
        return "Respond as a robot and say 'beep boop' a lot."

agent = Agent(
    name="Chat agent",
    instructions=custom_instructions,
)

async def main():
    context = CustomContext(style="pirate")
    result = await Runner.run(agent, "Tell me a joke.", context=context)
    print(result.final_output)
```

## Key notes

- `instructions` can be a `str` or `Callable[[RunContextWrapper[T], Agent[T]], str]`
- The callable may also be async: `async def my_instructions(ctx, agent) -> str:`
- Context object is typed; use `Agent[CustomContext]` for type-checked access
