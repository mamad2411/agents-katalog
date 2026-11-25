---
name: orchestration
# prettier-ignore
description: "Coordinate parallel agent work. Use when decomposing complex tasks, running review/implementation in parallel, managing task lists, or choosing shared vs isolated workspaces."
metadata:
  last_updated: "2026-07-04"
  verified_against: "current local skill refresh"
---

# Orchestration

Coordinate multi-agent or multi-session coding work without duplicated effort, context loss, or unnecessary integration overhead. Stay harness-agnostic: use whatever task, teammate, subagent, or mailbox primitives are available, and keep git worktrees as an explicit isolation choice rather than the default.

## When to Use

- Complex work that can split by domain, file area, or risk level
- Parallel review, research, testing, or documentation passes
- Background investigation while the lead preserves high-value context
- Risky changes where isolation may be worth the setup and merge cost

## Core Rules

- Assign clear ownership: one agent/session owns each file or subsystem.
- Keep the lead session responsible for synthesis, review, and final decisions.
- Prefer one mutating worker in the shared cwd/current branch unless parallel edits are clearly independent.
- Use parallel workers freely for read-only research, review, logs, CI, or test investigation.
- Create a shared task list with dependencies and acceptance criteria.
- Require concise handoff notes: files touched, decisions made, validation run, blockers.
- If the harness supports read-only/mutating flags, mark file-editing workers as mutating.

## Workspace Choice

Default to the current shared workspace for small, sequential, or tightly-coupled changes. It keeps local env, ignored files, ports, databases, and devcontainers intact.

Use isolated workspaces — git worktrees, cloned checkouts, containers, VMs, or cloud previews — only when the isolation benefit beats setup/runtime/integration cost.

Before choosing a worktree, answer:

- How are ignored files, dependencies, `.env`, generated files, and package caches handled?
- Are ports, databases, queues, and local services isolated?
- Who integrates the branch/patch and resolves semantic conflicts?
- How is cleanup handled after review?

## Decomposition Patterns

| Pattern              | Use when                                |
| -------------------- | --------------------------------------- |
| Fan-out              | Same operation across independent areas |
| Pipeline             | Research → implement → test → docs      |
| Reviewer/implementer | One session changes, another critiques  |
| Speculative branches | Trying competing approaches safely      |
| Background monitor   | Long-running CI, logs, or investigation |

## References

- [patterns.md](references/patterns.md) - Orchestration patterns
- [domains.md](references/domains.md) - Domain-specific decomposition
- [task-management.md](references/task-management.md) - Dependencies, task graphs, file partitioning
- [worktree-commands.md](references/worktree-commands.md) - Git worktree command reference
- [session-strategies.md](references/session-strategies.md) - Multi-session patterns
- [cleanup.md](references/cleanup.md) - Worktree removal and maintenance
