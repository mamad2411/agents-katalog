---
name: agent-implementer
disable-model-invocation: true
description: >-
  Delegate task to a coding agent (OpenCode or Codex) for
  implementation.
license: MIT
compatibility: >-
  Requires `opencode` or `codex` CLI installed and authenticated, or a running
  OpenCode server (`opencode serve`), git.
metadata:
  version: 0.1.0
---

# Task Implementer

Delegate a bounded task to a coding agent. You send one **brief** and run the **loop** below;

the agent works in a fresh session with no shared context.

## When to delegate vs. do it yourself

An implementer is a tool, not the default. Delegate only when both hold:

1. Delegation saves context or tokens.
2. Only the final result matters — intermediate steps have no lasting value.

## 0. Choose the implementer

Ask: "Which implementer? (OpenCode CLI, OpenCode Server, or Codex CLI)". Record it —
it stays fixed for the loop.

If OpenCode Server, ask for host and port (default `127.0.0.1:4096`).

## Prerequisites

Run the chosen CLI's `preflightCheck`. If unavailable or unauthenticated, report and
stop — do not install it.

## The loop

Simple tasks: one round. Complex: plan upfront, then multiple rounds.

### 1. Select a task group

Default parallel for independent groups; serial only where updates overlap. Parallel
groups must be non-overlapping (files, commands) — if two tasks share `Task A`, do
`Task A` first, then the rest serially.

### 2. Construct the brief

Build the brief from project facts using the template at
[references/writing-the-brief.md](references/writing-the-brief.md).

### 3. Dispatch and capture session

Dispatch `dispatchBrief` (or `resumeSession` to continue) from the matching operations
reference below; capture the session ID it returns.

### 4. Review

For parallel tasks, wait for all to finish, then review against their reports and the
git diff.

### 5. Land or rework

Correct → mark done.

Needs work → `resumeSession` back to the agent, or do
it yourself.

### 6. Next round or finish

Next round: `git add` the prior round so the next `git diff` is clean, then return to step 1.

Finished: report full status.

Blocked: end and report status plus the problem details.

## References

- [references/writing-the-brief.md](references/writing-the-brief.md) — brief template and
  report contract.
- Operations by driver — query `preflightCheck`, `dispatchBrief`, `extractSessionId`,
  `readReport`, `resumeSession` there:
  - [references/opencode-operations.md](references/opencode-operations.md) — OpenCode CLI
  - [references/opencode-server-operations.md](references/opencode-server-operations.md) — OpenCode Server API
  - [references/codex-operations.md](references/codex-operations.md) — Codex CLI
