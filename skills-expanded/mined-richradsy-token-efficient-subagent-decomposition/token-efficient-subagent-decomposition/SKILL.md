---
name: token-efficient-subagent-decomposition
description: Use when the user explicitly asks for subagents, delegation, parallel agents, or multi-agent orchestration. Helps decide if delegation is worth it, split bounded tasks, and keep handoffs cheap.
---

# Token Efficient Subagent Decomposition

## Guardrail

Only spawn subagents on explicit user request. Otherwise use the same routing logic but keep the work local.

## Routing Rule

Default to single-agent execution.

Delegate only when the task is:

- clearly bounded
- non-blocking for the very next local step
- low-coupling with evolving local context
- likely to benefit from parallelism more than it costs in coordination
- defined by a crisp output contract

Otherwise keep it local.

Treat the immediate blocking task as local by default.

## Workflow

1. Form a short local plan first.
2. Mark remaining tasks as `independent`, `parallelizable`, or `local`.
3. Keep the critical-path task local.
4. Delegate only independent side work with explicit ownership and output format.
5. Continue non-overlapping local work while subagents run.
6. Integrate returned results quickly and avoid redoing delegated work.

## Handoff Template

Prefer this handoff shape:

```text
Goal:
Scope:
Owned files or subsystem:
Known facts:
Open question:
Required output:
Constraints:
```

Do not pass raw transcript unless absolutely necessary.

For coding workers, always specify ownership, write scope, exact return artifact, and that they are not alone in the codebase and must not revert others' edits.

## Coordination Rules

- one coordinator, specialized side workers, no free-form all-to-all chat
- synchronize on completion, contradiction, risk spike, or merge point
- pass facts, diffs, and decisions, not narrative history
- use a reviewer only for high-risk or high-ambiguity work
- stop low-value branches early
- use fewer workers than feels comfortable

## When To Read More

Read [references/patterns.md](references/patterns.md) only when you need concrete delegation patterns, anti-patterns, or a compact spawn prompt template.
