---
name: forcing-tool-use
description: Force the model to call a specific tool or any tool on the first turn using tool_choice in ModelSettings.
category: agents
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [openai-agents, tool-choice, model-settings, forced-tool, reset-tool-choice]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: examples/agent_patterns/forcing_tool_use.py
imported_at: 2026-04-18T00:00:00Z
---

# forcing-tool-use

Set `model_settings=ModelSettings(tool_choice="required")` to force the model to call at least one tool. Use `tool_choice={"type": "function", "name": "my_tool"}` to force a specific tool.

## When to apply

When you need the agent to always use a tool on its first turn (e.g., always search before answering, always validate input). Prevents the model from skipping the tool and answering directly.

## Core snippet

```python
from agents import Agent, ModelSettings, function_tool

@function_tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for relevant information."""
    return f"Results for: {query}"

# Force any tool call
agent = Agent(
    name="Research assistant",
    instructions="Always search before answering.",
    tools=[search_knowledge_base],
    model_settings=ModelSettings(tool_choice="required"),
    reset_tool_choice=True,  # Default: reset after first tool call to avoid loops
)

# Force a specific tool
agent_specific = Agent(
    name="Search assistant",
    tools=[search_knowledge_base],
    model_settings=ModelSettings(
        tool_choice={"type": "function", "name": "search_knowledge_base"}
    ),
    reset_tool_choice=True,
)
```

## Key notes

- `tool_choice="required"`: model must call at least one tool
- `tool_choice="auto"`: model decides whether to call a tool (default)
- `tool_choice="none"`: model cannot call any tool
- `reset_tool_choice=True` (default): resets `tool_choice` to `"auto"` after the first tool call to avoid infinite tool loops
- Set `reset_tool_choice=False` if you want every turn to require a tool call
