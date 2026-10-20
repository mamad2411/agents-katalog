---
name: agent-lifecycle-hooks
description: Attach RunHooks and AgentHooks to observe and react to agent lifecycle events.
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, hooks, lifecycle, observability]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: examples/basic/lifecycle_example.py
imported_at: 2026-04-18T00:00:00Z
---

# agent-lifecycle-hooks

Implement `RunHooks` (run-level) or `AgentHooks` (agent-level) to observe agent start/end, LLM calls, tool calls, and handoffs. Pass hooks to `Runner.run(hooks=...)` or `Agent(hooks=...)`.

## When to apply

Logging, usage tracking, debugging, or triggering side effects (e.g., saving state) at each lifecycle step. Alternative to custom tracing processors for lightweight observation.

## Core snippet

```python
from agents import Agent, RunHooks, AgentHooks, RunContextWrapper, AgentHookContext, Tool, Runner

class ExampleHooks(RunHooks):
    async def on_agent_start(self, context: AgentHookContext, agent: Agent) -> None:
        print(f"Agent {agent.name} started. Input: {context.turn_input}")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output) -> None:
        print(f"Agent {agent.name} ended with: {output}")

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        print(f"Tool {tool.name} called")

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str) -> None:
        print(f"Tool {tool.name} result: {result}")

    async def on_handoff(self, context: RunContextWrapper, from_agent: Agent, to_agent: Agent) -> None:
        print(f"Handoff: {from_agent.name} -> {to_agent.name}")

hooks = ExampleHooks()

async def main():
    agent = Agent(name="Assistant", instructions="Be helpful.")
    result = await Runner.run(agent, "Hello!", hooks=hooks)
```

## Key notes

- `RunHooks` applies to the entire run; `AgentHooks` scopes to a single agent
- `on_tool_start/end` only fires for local function tools, not hosted tools
- `context.usage` tracks cumulative token usage across the run
- `context.turn_input` in `on_agent_start` gives the agent's current input
