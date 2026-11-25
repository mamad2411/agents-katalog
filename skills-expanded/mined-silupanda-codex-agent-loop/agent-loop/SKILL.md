---
name: agent-loop
description: Run bounded, resumable OpenAI-native coding loops with shell and apply_patch, similar to Claude Code agent loops. Use when the user asks for a loop, autonomous iteration, or a persistent inspect-edit-test cycle with a turn cap.
---

# Agent Loop

Use this skill for multi-step coding tasks that need a bounded agent loop instead of a single local step.

## When to use

- The user says loop, agent loop, autonomous, keep iterating, or mentions Claude Code.
- The work will likely require repeated inspect/edit/test cycles.
- A turn cap or explicit approval boundary is useful.

## Defaults

- `--max-turns 8`
- `--approval-mode on-write`
- `--model gpt-5.4`
- `--reasoning-effort high`

Important:

- Agent Loop is **bounded**. It should stop when the task looks complete, when it hits its turn/time budget, when it pauses for approval, or when an error occurs.
- In fallback mode without `OPENAI_API_KEY`, Agent Loop runs one `codex exec` session. That session may finish on the first turn for short read-only tasks.
- A stop reason like `completed_via_fallback` means the task completed through the fallback backend; it does **not** mean the run failed.

Shorthand budgets are also supported:

- `10m` = 10 minutes
- `1h` = 1 hour
- `5t` = 5 turns

## Invocation

Prefer invoking the bundled skill directly:

```text
$agent-loop <task>
```

Or with a shorthand budget:

```text
$agent-loop 10m <task>
```

Some Codex builds may also surface the plugin command definition. If yours
does, the equivalent command is:

```text
/agent-loop:run <task>
```

## Onboarding helpers

- `--doctor` checks that the plugin is installed and ready in Codex.
- `--demo` runs a safe read-only first-run example and suggests next commands.
- `10m`, `1h`, and `5t` work as shorthand budgets before the task text.

Approval modes in plain English:

- `on-write` = safe
- `never` = hands-off
- `always` = review-everything

## Approval behavior

- `on-write` auto-runs read-only shell inspection commands.
- `on-write` pauses before write-like shell commands and all patches.
- Use `--resume <state-file> --approve-pending` only after the user explicitly approves the paused action.

## Run artifacts

The runner stores logs and resumable state under:

`~/.codex/agent-loop/runs/`
