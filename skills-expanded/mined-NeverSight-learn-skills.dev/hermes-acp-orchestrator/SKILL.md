---
name: hermes-acp-orchestrator
description: Use when you need ACP-style delegation in Hermes with explicit agent routing to hermes, codex, or claude-code, including safe output limits and timeout-aware execution.
version: 1.0.0
author: Rainhoole
license: MIT
metadata:
  hermes:
    tags: [acp, delegation, orchestration, codex, claude-code]
---

# Hermes ACP Orchestrator

## Overview

Use this skill when tasks should be delegated through a single ACP-style pattern while keeping context isolated and results bounded.

Targets supported by delegation:
- `hermes` (default in-process subagent)
- `codex` (external Codex CLI)
- `claude-code` (external Claude Code CLI)

## When to Use

Use this skill when:
- You want deterministic routing to a specific agent.
- You want mixed-agent batch delegation.
- You need timeout and output-size guardrails for external agents.
- You want concise summaries returned to the parent turn.

Avoid this skill when:
- A single direct tool call is enough.
- The task is purely mechanical and better handled by `execute_code`.

## Delegation Patterns

### 1) Single task with explicit target

```python
delegate_task(
    goal="Implement the bugfix and run tests",
    context="Keep patch minimal and include changed files in the summary.",
    agent="codex"
)
```

### 2) Parallel batch with per-task agent override

```python
delegate_task(tasks=[
    {"goal": "Find regressions", "agent": "claude-code", "toolsets": ["file"]},
    {"goal": "Implement fix and validate", "agent": "codex", "toolsets": ["terminal", "file"]},
    {"goal": "Produce merge-ready summary", "agent": "hermes", "toolsets": ["file"]}
])
```

### 3) Reliability-focused run

```python
delegate_task(
    goal="Refactor auth middleware",
    context="Run focused tests and report failures only.",
    agent="claude-code",
    max_iterations=30
)
```

## Operating Rules

1. Always provide concrete `context` (file paths, constraints, expected output).
2. Keep tasks narrow; split large objectives into batch tasks.
3. Use `toolsets` to reduce accidental side effects.
4. Ask for structured summaries (what changed, what passed, what failed).
5. For external agents, keep outputs concise and action-oriented.

## Recommended Delegation Config

```yaml
delegation:
  max_iterations: 50
  default_toolsets: ["terminal", "file", "web"]
  external_timeout_seconds: 900
  external_max_output_chars: 24000
```

## Troubleshooting

- **Unsupported agent**: use only `hermes`, `codex`, `claude-code`.
- **External agent timeout**: increase `delegation.external_timeout_seconds` or split the task.
- **Oversized responses**: lower verbosity in the delegated goal and rely on concise summaries.
- **Weak results**: provide stronger context, acceptance criteria, and exact files to touch.
