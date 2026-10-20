---
name: run-config-global-settings
description: Use RunConfig to set run-wide defaults for model, max turns, tracing, and guardrails.
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, run-config, model-settings, max-turns, tracing]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: src/agents/run_config.py
imported_at: 2026-04-18T00:00:00Z
---

# run-config-global-settings

Pass `RunConfig` to `Runner.run(run_config=...)` to set run-wide defaults that apply unless overridden by per-agent settings.

## When to apply

When you want consistent model defaults, turn limits, tracing, or input filters across all agents in a run without configuring each agent individually.

## Core snippet

```python
import asyncio
from agents import Agent, Runner, ModelSettings
from agents.run import RunConfig

run_config = RunConfig(
    model="gpt-4o-mini",                # Default model for all agents
    model_settings=ModelSettings(        # Default model settings
        temperature=0.5,
        max_tokens=2048,
    ),
    max_turns=20,                        # Default is 10
    tracing_disabled=False,
    workflow_name="My Workflow",         # Name shown in Traces dashboard
    trace_include_sensitive_data=True,   # Include tool args/outputs in traces
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    # Agent-level model overrides RunConfig.model for this agent
    model="gpt-4o",
)

async def main():
    result = await Runner.run(agent, "Hello!", run_config=run_config)
    print(result.final_output)

asyncio.run(main())
```

## Key properties

| Property | Default | Description |
|---|---|---|
| `model` | `None` (agent's model) | Run-wide model override |
| `max_turns` | `10` | Max agent loop iterations |
| `tracing_disabled` | `False` | Disable traces for this run |
| `workflow_name` | `"Agent workflow"` | Name in Traces dashboard |
| `trace_include_sensitive_data` | `True` | Include args/outputs in traces |

## Key notes

- Per-agent `model` and `model_settings` override `RunConfig` values for that agent
- `RunConfig` is passed to `Runner.run()`, not stored on the Agent
- `call_model_input_filter` can intercept and modify the input before each model call
