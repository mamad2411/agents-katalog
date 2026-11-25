---
name: mentat-tasks
description: Local md task store. Atomic claim, TTL refresh, vertical-slice + HITL/AFK doctrine.
allowed-tools: Bash(python3 ~/.agents/skills/mentat-tasks/scripts/tasks.py *)
---

# mentat-tasks

Manage a local markdown task store backed by POSIX atomics. No server, no database, no binary. Each task is a file; each claim is a lock sentinel.

## Layout

Tasks live at `<repo>/.mentat/tasks/<ID>-{plan-ref}.md`. Cross-repo unified view: `ln -s ~/.mentat/tasks .mentat/tasks` (user runs once).

Board-home vs worktree separation (ADR-0002): task files live on the holding branch. Chunks operating in worktrees write status back via the atomic protocol below.

## Task file schema

```yaml
---
id: T001
status: todo            # todo | in-progress | review | done | wontfix
kind: HITL              # HITL | AFK — vertical-slice classification (required before pick)
claimed_by: ""          # agent id or empty
claim_expires_at: ""    # RFC3339; empty if unclaimed
created_at: 2026-06-06T00:00:00Z
---
```

Body sections:
- **Parent** — plan or PRD link.
- **What to build** — one paragraph.
- **Acceptance criteria** — bulleted checklist.
- **Blocked by** — prose, free-form.

## Invocation

All operations route through `scripts/tasks.py`. Set `MENTAT_TASKS_DIR` to override the default `.mentat/tasks/` dir.

| Subcommand | Args | Description |
|---|---|---|
| `next-id` | — | Print next `T###` |
| `create` | `{plan-ref}` | reads stdin | Create task file from stdin body |
| `claim <file> <agent> <ttl_s>` | — | Atomic claim via O_EXCL lock sentinel |
| `release <file>` | — | Release claim, restore `todo` |
| `refresh <file> <ttl_s>` | — | Bump `claim_expires_at` |
| `done <file>` | — | Terminal state: done |
| `wontfix <file>` | — | Terminal state: wontfix |
| `list [--status <s>]` | — | Enumerate tasks as TSV (id, status, kind, claimed_by) |

## Atomic-write invariant

All frontmatter mutations use `lib.support.frontmatter.mutate` — tmp+`os.replace` same-fs rename (POSIX `rename(2)`). Claims use `os.open(O_CREAT|O_EXCL)` for exclusive create — correct POSIX primitive for test-and-set. The lock sentinel (`.lock`) is separate from the content file so rename never rebinds the guard inode.

## Pick gate

Pick only if:
1. `status` is `todo`, or `in-progress` with `claim_expires_at < now` (stale — release then re-claim).
2. `kind` is set (`HITL` or `AFK`). Never pick untriaged.
3. No `.lock` sentinel exists for a non-expired claim.

## Events emitted

| Event | Payload |
|---|---|
| `task_created` | `{id, slug}` |
| `task_claimed` | `{id, agent, expires_at}` |
| `task_released` | `{id}` |
| `task_resolved` | `{id}` |
| `task_canceled` | `{id}` |

## Boundary with other skills

Intake skill → writes task via `mentat-tasks create`.
`triage` → mutates `kind` + `status`.
`mentat-prd` → references task ids as `T###` in prose.
`mentat-tasks` owns schema + filesystem protocol only.

## Deferred

Typed dep graph, `touches:` write-set lease, priority/tags/due/estimate. Add only on demonstrated need.
