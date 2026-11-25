---
name: deferred-tool-loading
description: Defer large tool surfaces until runtime with defer_loading=True and ToolSearchTool to reduce upfront token usage.
category: agents
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [openai-agents, tool-search, deferred-loading, token-efficiency, tool-namespace]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: docs/tools.md
imported_at: 2026-04-18T00:00:00Z
---

# deferred-tool-loading

Mark tools with `defer_loading=True` in `@function_tool`, group them into a `tool_namespace`, and add `ToolSearchTool()` to the agent. The model loads only the tools it needs per turn.

## When to apply

Agents with many tools (>20) where including all tool schemas upfront wastes tokens. The model searches for and loads only the relevant tools each turn.

## Core snippet

```python
from typing import Annotated
from agents import Agent, Runner, ToolSearchTool, function_tool, tool_namespace

@function_tool(defer_loading=True)
def get_customer_profile(customer_id: Annotated[str, "The customer ID."]) -> str:
    """Fetch a CRM customer profile."""
    return f"profile for {customer_id}"

@function_tool(defer_loading=True)
def list_open_orders(customer_id: Annotated[str, "The customer ID."]) -> str:
    """List open orders for a customer."""
    return f"open orders for {customer_id}"

crm_tools = tool_namespace(
    name="crm",
    description="CRM tools for customer lookups.",
    tools=[get_customer_profile, list_open_orders],
)

agent = Agent(
    name="Operations assistant",
    model="gpt-4o",  # Requires Responses API model
    instructions="Load the crm namespace before using CRM tools.",
    tools=[*crm_tools, ToolSearchTool()],
)
```

## Key notes

- `defer_loading=True` marks the tool as deferred; it is not sent to the model until loaded
- `tool_namespace()` groups deferred tools; the model loads the namespace first
- `ToolSearchTool()` is required to enable dynamic tool loading
- Only works with OpenAI Responses API models that support tool search
- Reduces initial prompt tokens when you have many tools
