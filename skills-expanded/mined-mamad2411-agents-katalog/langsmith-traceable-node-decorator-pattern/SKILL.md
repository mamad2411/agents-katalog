---
name: langsmith-traceable-node-decorator-pattern
description: Wrap each LangGraph node function with @traceable(name=...) so every step appears as a discrete child run in LangSmith, plus emit semantic LLM run_names via with_config so individual model calls are labelled too.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [langsmith, traceable, observability, langgraph]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/nodes/investigate/node.py
imported_at: 2026-04-18T00:00:00Z
---

# LangSmith Traceable Node Decorators

## When to use
You want every LangGraph node to surface as a labelled span in LangSmith without sprinkling manual `Client.create_run` calls. You also want each LLM call inside a node to appear with a human-readable name so a 30-step trace is browsable.

## How it works
- Apply `@traceable(name="node_xxx")` to each pure node function. LangSmith picks up inputs and outputs automatically.
- Inside nodes, use `llm.with_config(run_name="LLM – Analyze evidence and propose root cause").invoke(prompt)` so each model call gets its own readable label in the trace UI.
- Pair with the LangGraph `astream_events` mapping: the framework already attaches `langgraph_node` to event metadata, so `metadata.langgraph_node` matches the `@traceable` name.

## Example
```python
from langsmith import traceable

@traceable(name="node_investigate")
def node_investigate(state):
    # ... pull planned_actions, etc.
    execution_results = execute_actions(...)
    return {...}

@traceable(name="node_diagnose_root_cause")
def node_diagnose_root_cause(state):
    return diagnose_root_cause(state)

# Inside a node, label individual LLM calls:
response = llm.with_config(
    run_name="LLM – Analyze evidence and propose root cause"
).invoke(prompt)
```

## Gotchas
- `@traceable` decorates pure functions — if your node mutates state in place, return a dict so LangSmith sees the delta.
- Use a consistent `node_*` naming so dashboards can filter/aggregate.
- Combine with `langsmith` env vars (`LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`) — when not configured, `@traceable` is a no-op so it's safe in CI/local dev.
- For sub-LLM calls, prefer descriptive `run_name` strings ("LLM – Classify + extract alert") over raw model names; the trace becomes a story.
