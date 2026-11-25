---
name: catch-up
description: Cross-project command center — scans every project's saved session states and checkpoints and shows all your open work and next actions in one dashboard. For when you've lost track of what's in flight across everything.
allowed-tools: Bash, Read, Glob
argument-hint: [optional: filter, e.g. "stale" or a project name]
---

# Catch-up

Build one dashboard of everything the user has in flight across ALL their
projects, pulled from the per-project memory stores. The user juggles many
projects and needs a single bird's-eye view, not a per-project dig.

## Step 1 — Find all the state files

Across every project's memory folder — `~/.claude/projects/*/memory/` — collect
(Bash/Glob):
- every `session_state_*.md`
- every `compact_checkpoint.md`

Exclude anything under an `archive/` subfolder.

## Step 2 — Extract only the essentials from each

Use **targeted extraction** (grep/sed for the frontmatter and the relevant
section lines) — **not** full-file Reads. With dozens of files across many
projects, reading each in full would blow your context. Pull only:
- **Project** — a readable name derived from the folder (the last meaningful
  segment(s) of the decoded path, e.g. `…-projects-my-app` → "my-app").
- **What** — the topic/description.
- **Next action** — the single next step (from "Next action" / "Immediate" /
  "Current Status").
- **Last touched** — the `created:` date (fall back to file mtime if absent).
- **Type** — session-state vs **active compact-checkpoint** (a checkpoint means
  a task was mid-flight at a compact and never closed out).

## Step 3 — Present the dashboard

Sort most-recently-touched first. Group into:

**Active (touched ≤ 14 days)** — table: Project | What | Next action | Last touched
**Stale (older)** — same columns, condensed; these are candidates to finish or archive.

Surface any **active checkpoint** at the very top — that's interrupted work.

If the user passed an argument, filter to it (a project name, or `stale` /
`active`).

## Step 4 — Close with a nudge

One line: how many open threads total, and your pick for the single most worth
resuming next (most recent, or most important-but-going-stale). A nudge, not a
lecture.

Keep the whole thing scannable — this is a dashboard, not a report. Read-only;
never modify the state files.
