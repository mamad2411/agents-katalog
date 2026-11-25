---
name: issue-basics
description: >
  Everyday single-issue CRUD over the `forge issue` verbs:
  create/update/show/list/search/close/reopen/comment, set priority/labels/assignee, claim or
  release one issue, add/remove dependency edges, plus backlog `stats`. Use for ANY routine
  one-off issue op: "create an issue/bug/task for X", "update/edit issue <id>", "close or
  reopen this issue", "comment a handoff note on <id>", "list/filter open bugs by
  status/label/priority", "bump this to P1", "reassign to alice", "mark <id> blocked by <id>".
  Also the parity floor migrating off a Beads-style tracker (label/reopen/delete map to forge
  equivalents). Single-operation plumbing only. Does NOT choose, rank, or explain the next
  issue to work on or why it's blocked (use triage-ready); does NOT run
  claim-then-prove-lease-ownership safety (use claim-safety); does NOT drive an issue through
  the plan->dev->validate->ship pipeline or open a PR (use smith or stage skills); does NOT
  report the current stage or what's in flight (use status).
allowed-tools: Read, Bash(forge:*)
terminal: true
---

# Issue basics — the CRUD floor

Everyday issue operations over the Forge kernel. Every command here is a real
`forge issue` verb (confirm with `forge issue --help`). The kernel is the single
source of truth — never hand-edit the issue store.

Every `--json` reply is the same envelope: `{ ok, schema_version, command, data,
next_commands }` on success, or `{ ok:false, error:{ message, exit_code } }` on
failure. **Gate on `ok`** — do not parse `data` until you confirm `ok:true`.

## The core loop

| Need | Command |
|------|---------|
| Create an issue | `forge issue create --title "…" --type <task\|bug\|epic\|decision>` |
| Inspect one issue | `forge issue show <id> [--json]` |
| List / filter issues | `forge issue list [--status … --type … --priority … --label …] [--json]` |
| Full-text search | `forge issue search "…" [--json]` |
| Backlog counts | `forge issue stats [--json]` |
| Claim work (DB-enforced lease) | `forge issue claim <id>` |
| Release a claim | `forge issue release <id>` |
| Update fields | `forge issue update <id> [flags]` |
| Add a handoff note | `forge issue comment <id> "…"` |
| Close (one or many) | `forge issue close <id...> --reason "…"` |
| Dependencies | `forge issue dep add\|remove <id> <blocks-id>` |

## Create — the flags that matter

```bash
forge issue create --title "Add rate limiting" --type task \
  --priority P1 --label "feature,api,security" --assignee alice \
  --acceptance "429 returned after N req/min; covered by a test"
```

| Flag | Meaning | Default |
|------|---------|---------|
| `--title "…"` | Human title (a bare leading positional also works) | minted id |
| `--type <…>` | `task` · `bug` · `epic` · `decision` | `task` |
| `--priority <…>` | `P0`..`P4` (or bare `0`..`4`); `P0` is highest | unset |
| `--label "a,b"` | Comma-separated set — one flag, split on `,` (repeats do NOT accumulate) | none |
| `--body "…"` | Long description (`--description` is an accepted alias) | empty |
| `--assignee <who>` | Persistent assignee | unset |
| `--acceptance "…"` | Acceptance criteria (`--design`, `--notes` also persist) | unset |
| `--parent <id>` | Parent/epic id | none |

`--status` defaults to `open`. Status vocabulary: `open` · `in_progress` ·
`review` · `done` · `cancelled`. Unlike `--priority` and `--status` (which reject
unknown values), `--type` is stored verbatim — a non-canonical value like
`feature` is accepted without error but carries no kernel behaviour, so stick to
the four canonical types. Epics and decisions are excluded from the ready queue
(non-claimability is a queue convention, not enforcement — `forge issue claim`
currently returns `ok:true` on them too).

## Update — same field flags, plus close

`forge issue update <id>` takes `--status`, `--title`, `--body`/`--description`,
`--priority`, `--label` (reparents the whole set), `--parent`, `--assignee`,
`--acceptance`, `--design`, `--notes`. `forge issue close <id> --reason "…"`
records the reason on the close event and accepts multiple ids in one call.

## Migrating from a Beads-style tracker — verb disposition

Nothing you relied on silently disappears; a few verbs map onto a `forge` flag or
are intentionally unsupported:

| Old verb | Forge equivalent |
|----------|------------------|
| `label` (add/remove) | **No subcommand** — pass the full set via `--label "a,b"` on `create`/`update` (last-value-wins). |
| `reopen` | `forge issue update <id> --status open`. |
| `delete` | **Unsupported by design** — the kernel is append-only/event-sourced. Use `forge issue close <id> --reason "…"` instead. |

## Reliability

- **Check `ok` before trusting output.** On `ok:false`, read `error.message` and
  fix the input rather than retrying blindly.
- **Claim before you mutate shared work.** `forge issue claim <id>` takes a
  DB-enforced lease; hand off to the `claim-safety` procedure before acting on a
  claimed issue you intend to change. `forge issue release <id>` if you abandon it.
- **Record decisions as comments, not memory.** `forge issue comment <id> "…"`
  survives the session; scratch notes do not.

## Fork points

Editable conventions — set these once for your team and this skill enforces them.
It is a canonical source you fork, not a fixed policy.

| Knob | Default | How to change |
|------|---------|---------------|
| **Default type** | `task` (kernel default) | Decide your create convention — e.g. always pass `--label feature` for user-facing work (feature is a label, not a canonical type), `--type bug` for regressions. |
| **Default priority** | unset | Adopt a house scale (e.g. new work opens at `P2`, incidents at `P0`) and always pass `--priority`. |
| **Fields required on create** | `--title` only | Require `--acceptance` (and `--label`/`--assignee`) on every create so issues are actionable from birth. |
| **Id / reference convention** | kernel-minted ids | Standardize how you cite issues in commits/PRs (e.g. `Closes <id>`) and whether you pass an explicit `--id`. |
| **Label taxonomy** | free-form | Pin an allowed label set your team agrees on and pass it consistently via `--label "a,b"`. |
