---
name: function-tool-registration
description: Register a Python function as an agent tool using the @function_tool decorator.
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, tools, function-tool, pydantic]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: examples/basic/tools.py
imported_at: 2026-04-18T00:00:00Z
---

# function-tool-registration

Wrap any Python function as a callable tool using `@function_tool`. The decorator introspects the function signature and docstring to build the JSON schema automatically. Pydantic models work as return types.

## When to apply

Use when an agent needs to call a local Python function — fetch data, compute a result, call an external API — within a single agent turn.

## Core snippet

```python
from typing import Annotated
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool

class Weather(BaseModel):
    city: str = Field(description="The city name")
    temperature_range: str
    conditions: str

@function_tool
def get_weather(city: Annotated[str, "The city to get the weather for"]) -> Weather:
    """Get the current weather information for a specified city."""
    return Weather(city=city, temperature_range="14-20C", conditions="Sunny with wind.")

agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
```

## Key notes

- Docstring becomes the tool description visible to the LLM
- `Annotated[type, "description"]` annotates individual parameters
- Pydantic models are automatically serialized/deserialized
- Async functions work equally: `async def my_tool(...) -> str:`
- Access run context via first param: `def my_tool(ctx: RunContextWrapper[MyContext], ...):`
