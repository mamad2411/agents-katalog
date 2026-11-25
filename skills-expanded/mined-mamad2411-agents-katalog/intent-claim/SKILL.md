---
name: intent-claim
description: Create, renew, list, or release an ephemeral Git-common-dir lease for genuinely parallel work sharing a semantic scope, interface, or path. Planning normally manages claims automatically.
---

# intent-claim

Claims coordinate current execution. They contain no decisions, never enter a commit, and are
unnecessary for serial or disjoint work.

## Invocation

```text
/intent-claim <unit> [--lease 2h] [--scope dotted.scope] [--paths paths...] [--interfaces names...]
/intent-claim --renew <unit> [--lease 2h]
/intent-claim --release <unit>
/intent-claim --list [--scope dotted.scope]
```

`intent-plan` should create and release claims for planned work. Use this skill directly when
parallel work began independently.

Before creating one, confirm another live unit intersects by scope, named interface, or actual
changed path. If not, report `claim unnecessary`. Never overwrite a different live owner.

## Store

Resolve `COMMON=$(git rev-parse --git-common-dir)` and write
`$COMMON/intent/claims/<unit>.yml`:

```yaml
version: 1
unit: requester-chat
owner: codex/requester-chat-repair
branch: codex/requester-chat-repair
worktree: /absolute/path/to/worktree
task: local:session-id
scope: requester.intake
interfaces: [RequesterTurn->RequestDraft]
paths: [frontend/src/components/StartMask.tsx]
created: 2026-08-27T10:00:00Z
renewed: 2026-08-27T10:00:00Z
expires: 2026-08-27T12:00:00Z
```

Use UTC RFC 3339 timestamps and a two-hour default lease. Renewal preserves `created`; release
deletes exactly one unit file.

Before list, create, or compile, delete a claim only when liveness failure is conclusive: expiry
with no active task, merged branch, absent or prunable worktree, or missing branch with no active
task. Use ancestry, never dates, for merge state. Do not infer remote activity from stale refs.

Overlap affects scheduling and produces a warning. It never establishes a semantic contradiction
or authorizes selecting one side of a conflict.
