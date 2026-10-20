---
name: triage-ready
description: >
  Surfaces, ranks, and EXPLAINS the single best next issue in a Forge project — strictly
  read-only. Recomputes the live ready queue and explains what is blocked via `forge issue
  ready`/`blocked`/`stats`/`show`, always against the live kernel, never `forge board`.
  Recommends ONE issue with a one-line reason, then hands off; never claims, comments, closes,
  or mutates. Use when the user asks "what should I work on", "what's next", "what's ready",
  "pick/triage my next task", "top of the ready queue", "which issue should I start", "why is
  this issue blocked", or "what's blocking the most work". NOT for claiming or taking
  ownership of the pick (use claim-safety), not for everyday issue
  create/update/list/search/close/comment/dep CRUD (use issue-basics), not for reporting the
  current workflow stage or "where am I / what's in flight" (use status), not for orienting a
  whole session or routing to stage skills (use kernel), not for driving an issue to a merged
  PR (use smith).
allowed-tools: Read, Bash(forge:*)
next: claim-safety
terminal: false
---

# Triage: what should I work on next

A read-only orientation skill. It answers "what is the single best thing to work
on right now, and *why*?" and hands the pick off to `claim-safety` / `dev` — it
never mutates the store itself.

Readiness in the Forge kernel is a **derived read model**: an issue is ready only
when every dependency is satisfied, it is unclaimed (no live lease), it is a
claimable type (epics and decisions never enter the queue), and no defer window
holds it back. Because it is derived, **always recompute it** — never trust a
cached "status == ready". Recompute means: run the query fresh each time.

## Do NOT use `board`

`forge board` reads a legacy snapshot store, not the live kernel, so its readiness
can be stale or wrong. This skill uses `forge issue ready`, `forge issue blocked`,
and `forge issue stats` exclusively.

## Procedure

### 1. Take the pulse

```bash
forge issue stats --json
```

Returns `data.counts` (`open`/`done`/`cancelled` — keys are present only when
non-zero, and there is no `in_progress` bucket: claimed work stays in status
`open` and is surfaced via `active_claims`), `ready_count`, `blocked_count`, and
`active_claims`. A high `blocked_count` relative to
`ready_count` is your signal that dependency repair (not new work) is the real
bottleneck — hand off to `dependency-planning` / `backlog-hygiene`.

### 2. Rank the ready queue

```bash
forge issue ready --json
```

`data.issues[]` comes back ordered by `rank` (priority ascending, then id), each
carrying `id`, `title`, `type`, `priority` (`P0`..`P4`), `rank`, `blocked`,
`claimed_by`, `parent_id`, `labels[]`, and `dependencies[]`. The top item is your
default pick. Surface the top few (see Fork points for how many), not the whole
list.

### 3. Explain WHY the top item is ready

Do not just name it — justify it. Pull its full record:

```bash
forge issue show <id> --json
```

State the reason in one sentence, drawn from the record:

- **Priority / rank** — `P0` at `rank` 0 outranks everything below it.
- **Dependencies satisfied** — every id in `dependencies[]` is closed/done, so
  nothing gates it (`blocked: false`).
- **Unclaimed** — `claimed_by` is `null`, so no other agent holds the lease.
- **Claimable type** — it is a `task`/`feature`/`bug`, not an `epic`/`decision`.

### 4. Explain why the runners-up are NOT ready

```bash
forge issue blocked --json
```

For a blocked item, name the specific unmet dependency (from its `dependencies[]`
cross-referenced against `forge issue show`) — e.g. "blocked by `forge-x` which is
still `open`". This turns triage into an actionable map: the fastest way to unlock
the most work is usually to finish the shared blocker.

### 5. Hand off

Recommend ONE issue with its one-line justification, then stop. The caller claims
it (via `claim-safety`) and executes (via `dev`). Triage does not claim, comment,
or close — it is strictly read-only.

## Reliability

- **Recompute, never cache.** Readiness is derived; re-run `forge issue ready`
  every session rather than remembering a prior "ready" verdict.
- **Respect non-claimable types.** Epics and decisions never appear in `ready`
  (the queue surfaces only claimable types — `task`/`bug`), so do not hand them
  off as work. There is no `claimable` field in the CLI JSON; this is behavioral,
  not a flag you can read.
- **Check the envelope.** Every `--json` reply carries `ok`; on `ok:false` read
  `error.message` and retry the query rather than guessing at state.
- **Read-only.** This skill runs only `stats`/`ready`/`blocked`/`show`. If a fix is
  needed, hand off — never mutate here.

## Fork points

Editable knobs — change these to carve your own triage policy. This skill is a
canonical source you fork, not a fixed ladder.

| Knob | Default | How to change |
|------|---------|---------------|
| **Readiness query / filters** | `forge issue ready` (whole queue) | Narrow to a slice, e.g. `forge issue list --status open --priority P0 --json` or post-filter `ready` output by `labels[]`/`type` to focus one workstream. |
| **How many items to surface** | Top 3 by `rank` | Raise for a broad standup view, lower to 1 for a strict "next task only" hand-off. |
| **Stale threshold** | `forge issue stale --days 14` | Change `--days` to flag idle in-progress work sooner/later; surface stale claims as a caveat before recommending fresh work. |
| **Priority ordering** | Kernel `rank` (priority, then id) | Re-rank the `ready` list by your own weights — epic proximity (`parent_id`), label, or age — before picking. |
| **Blocked-explain depth** | One hop (direct unmet deps) | Trace transitively via repeated `forge issue show` when you need the full blocking chain; hand to `graph-forensics` for deep `explain`. |
