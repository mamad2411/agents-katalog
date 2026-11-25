---
name: agent-structured-output
description: Configure an agent to return a Pydantic model as its final output instead of plain text.
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, structured-output, pydantic, output-type]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: examples/agent_patterns/deterministic.py
imported_at: 2026-04-18T00:00:00Z
---

# agent-structured-output

Set `output_type` on an `Agent` to a Pydantic `BaseModel`. The SDK enforces structured output and returns a typed instance via `result.final_output_as(MyModel)`.

## When to apply

When downstream code must parse the agent's reply (routing, classification, evaluation pipelines). Replaces fragile string parsing with typed data.

## Core snippet

```python
from pydantic import BaseModel
from agents import Agent, Runner

class OutlineCheckerOutput(BaseModel):
    good_quality: bool
    is_scifi: bool

outline_checker_agent = Agent(
    name="outline_checker_agent",
    instructions="Read the given story outline, and judge the quality. Also, determine if it is a scifi story.",
    output_type=OutlineCheckerOutput,
)

async def main():
    result = await Runner.run(outline_checker_agent, "A space opera about clones...")
    output = result.final_output_as(OutlineCheckerOutput)
    print(output.good_quality, output.is_scifi)
```

## Key notes

- `result.final_output` is the raw Pydantic model instance when `output_type` is set
- Use `result.final_output_as(MyModel)` for type-checked access
- The agent runs until it produces output matching the schema (strict JSON schema by default)
- Works with nested models and optional fields
