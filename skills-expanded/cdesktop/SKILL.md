---
name: cdesktop
description: Operate the cdesktop coding-session environment — agent teams, session management, file conventions.
---

# cdesktop

cdesktop spawns coding-agent sessions per workspace. You may be running as
a standalone session, or as part of a **team** in the same workspace.

## Agent Teams

Use this when delegating parallel subtasks, getting a second opinion, or
running a structured debate. Teammates share your working directory by
default — pick non-overlapping file scopes for write-heavy work.

### Commands

Canonical invocation is `npx cdesktop team ...` (works without global
install). If `cdesktop` is on your `PATH`, you may use it directly as a
shorthand.

- Spawn (lead only): `npx cdesktop team spawn --name <name> [--prompt-file p] [--executor ...] [--model ...] [--provider ...]`
- Send: `npx cdesktop team send <id> --message-file p`
- List: `npx cdesktop team list --json`

Every command requires the `CDESKTOP_SESSION_ID` env var, which cdesktop
injects automatically at executor spawn. If the var is missing, you are
running outside a cdesktop session and `team` commands will refuse.

### When to spawn

- Research from N angles in parallel.
- Parallel implementation on non-overlapping modules.
- Devil's advocate / critique against your plan.

### Roles

Free-text via `--name`. Common labels: `researcher`, `reviewer`,
`refactorer`, `debater`. The name is also the session's pill label in
the cdesktop UI, so prefer short (≤ 24 chars), descriptive names.

### Cross-executor / cross-model

Pass `--executor`, `--variant`, `--model`, `--reasoning`, `--provider`
to spawn a teammate using a different agent / model than yourself. When
you change executor you MUST pass `--model` and `--provider`, otherwise
the server returns `EXECUTOR_REQUIRES_PROVIDER`.

When you omit these flags, the teammate inherits your executor, model,
provider, reasoning effort, and permission mode.

### Peer messaging

Any team member can send to any other (including the lead). The
recipient's executor / model / provider are preserved — `send` never
swaps a teammate's config mid-stream. Encourage debate by spawning two
teammates with opposing prompts and forwarding their findings.

### Anti-patterns

- Don't spawn for trivial subtasks — the orchestration overhead exceeds
  the benefit.
- Don't have N teammates write the same file in parallel — overlapping
  writes will clobber each other. Pick non-overlapping module scopes.
- Watch for ping-pong loops; cut a thread by sending a final resolution
  message or stopping the session in the UI.
- Don't expect teammates to be synchronous — they run in their own
  process and respond when they finish their turn.

## (Future cdesktop sections)

Other cdesktop behaviours will be documented here as they ship.
