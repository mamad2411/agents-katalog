# Copilot Instructions: Building Ai Agents With Design Systems And Python
Description: A comprehensive skill for building AI agents that leverage design systems, context engineering, and Python frameworks like Agentspan. Includes workflows for agent creation, tool integration, and crash resilience.

## Overview
This skill teaches you how to build AI agents that integrate design systems and context engineering using Python and the Agentspan framework. You'll learn to define agents, create tools, and ensure resilience against crashes. For a deeper dive into core concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Install Prerequisites**: Ensure Python 3.10+, JDK, and uv are installed.
2. **Set Up Agentspan**: Initialize a project and add Agentspan dependencies.
3. **Define Tools**: Create Python functions with decorators to expose them to the agent.
4. **Configure the Agent**: Define the agent's name, model, and tool list.
5. **Run the Agent**: Use the Agentspan server to execute the agent.
6. **Ensure Resilience**: Implement idempotent tool calls and handle crashes gracefully.

## Code Snippets
```python
from agentspan import tool

@tool
def get_weather(city: str) -> str:
    """Returns the weather for a given city."""
    return f"Sunny in {city}"
```
For more examples, see [Code Examples](references/code_examples.md).

## Best Practices
- Always include docstrings and type hints in tool functions.
- Use idempotent tool calls to avoid duplicate results.
- Validate your setup with `uv run agentspan doctor`.

## Common Pitfalls
- Missing docstrings can confuse the agent.
- Non-idempotent tool calls can lead to duplicate data.
- Improper setup of AI providers can cause failures.

## Validation Steps
1. Run `uv run agentspan doctor` to check setup.
2. Execute the agent and verify tool calls in the Agentspan dashboard.
3. Test crash resilience by interrupting the agent mid-execution.

For a practical guide, see [Practical Guide](references/practical_guide.md).

## Reference Guides

### Code Examples

# Code Examples

## Tool Creation
Create tools with docstrings and type hints.

```python
from agentspan import tool

@tool
def get_weather(city: str) -> str:
    """Returns the weather for a given city."""
    return f"Sunny in {city}"
```

## Agent Configuration
Define the agent with a name, model, and tool list.

```python
agent = Agent(
    name="WeatherBot",
    model="openai/gpt-4-mini",
    tools=[get_weather]
)
```

## Running the Agent
Start the Agentspan server and execute the agent.

```bash
uv run agentspan server start
uv run main.py
```

## Crash Resilience
Implement idempotent tool calls and use execution IDs to resume tasks.

```python
if execution_id:
    runtime.resume(execution_id)
else:
    runtime.run(agent)
```

For a practical guide, see [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts

## Design Systems
A design system is a set of rules and building blocks that ensure consistency in software development. It includes components like fonts, UI elements, colors, and layout rules. Think of it as a Lego set with instructions—the instructions are the design system, and the blocks are the components.

## Context Engineering
Context engineering involves teaching an AI agent the necessary information before it starts a task. This is often done using the Model Context Protocol (MCP), which formats information for easy consumption by the AI.

## Agentic AI
Agentic AI refers to AI that can make decisions, choose actions, and use tools to accomplish tasks. It leverages design systems and context engineering to ensure accuracy and consistency.

## Agentspan Framework
Agentspan is a Python framework for building AI agents. It supports tool creation, agent configuration, and crash resilience. The framework runs agents on a server, making them resilient to client crashes.

For more details on practical applications, see [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide

## Setting Up
1. **Install Python 3.10+**: Ensure you have the correct Python version.
2. **Install JDK**: Necessary for running Agentspan.
3. **Install uv**: A package manager for Python dependencies.

## Creating Tools
Tools are Python functions that the agent can call. They must include docstrings and type hints to guide the agent.

```python
from agentspan import tool

@tool
def get_weather(city: str) -> str:
    """Returns the weather for a given city."""
    return f"Sunny in {city}"
```

## Configuring the Agent
Define the agent's name, model, and tool list. The model string should follow the format `provider/model_name`.

```python
agent = Agent(
    name="WeatherBot",
    model="openai/gpt-4-mini",
    tools=[get_weather]
)
```

## Running the Agent
Start the Agentspan server and run the agent. Use the dashboard to monitor executions.

```bash
uv run agentspan server start
uv run main.py
```

## Ensuring Resilience
Implement idempotent tool calls to handle crashes gracefully. Use execution IDs to resume interrupted tasks.

For code examples, see [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Bridging Design Systems and Code with MCP and AI Agents](https://www.youtube.com/watch?v=Gh1E9VgXZWs)** by IBM Technology
2. **[Build Your First AI Agent in Python (Step by Step)](https://www.youtube.com/watch?v=YKPO2S6j7MM)** by Kevin Stratvert