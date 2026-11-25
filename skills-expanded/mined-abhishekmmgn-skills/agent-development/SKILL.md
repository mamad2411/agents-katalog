---
name: agent-development
description: implementation patterns for Gemini agents. Use this for coding ReAct loops, defining tools in Python, and using frameworks like LangChain/LangGraph.
---

# Gemini Agent Development Patterns

## Goal
Implement robust agent loops and tool definitions using Python and standard agent frameworks.

## 1. Defining Tools (Function Calling Pattern)
To allow the model to use a tool, you must define its schema (signature) clearly.

**Python Example (Google GenAI SDK):**
```python
def display_cities(cities: list[str], preferences: str = None):
    """Provides a list of cities based on user preferences."""
    return cities

# Define the tool config
tool_config = types.ToolConfig(
    function_calling_config=types.FunctionCallingConfig(mode='ANY')
)

# Send to model
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="I want a ski trip...",
    tools=[display_cities],
    tool_config=tool_config
)
