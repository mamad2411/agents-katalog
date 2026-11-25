---
name: weekly
description: >-
  Mission Control weekly review. Drives the Sunday sweep: clear the Needs-Review
  queue, sweep open tasks by project (close/drop/re-prioritize), reset due dates for
  the week, and promote backlog items. Use when asked to "weekly review", "weekly",
  "review my week", "sweep my tasks", or "let's do the weekly".
---

# weekly — Mission Control weekly review

A guided sweep that keeps the system honest, so it doesn't decay between standups.
Run the agenda, then walk the user through each section with opinionated recommendations.

## Run the agenda

```bash
mc weekly            # human-readable agenda (or: python3 ~/mission-control/bin/weekly.py)
mc weekly --json     # structured, to act on
```

## Drive the review (interactive, in this order)

1. **① Needs Review** — every Claude-written task awaiting sign-off. For each: **accept**
   (flip `needs_review: false` in its file), **edit**, or **delete** (`trash`). Don't leave
   the queue full — an unswept Needs-Review pile is the #1 decay signal (29 sat unreviewed
   for the first 12 days of this vault's life).
2. **② By Project** — for each project's open tasks: close anything `done`, `cancelled` the
   stale, re-prioritize the rest. Propose specific changes; apply on the user's yes.
3. **③ Overdue** — for each, either reset `due`/`scheduled` to a real date this week or do it now.
4. **④ Backlog** — someday/maybe with no date. Promote one or two to active if there's room;
   leave the rest.

## How to apply changes

- Edit the task file's frontmatter directly (`status`, `priority`, `due`, `scheduled`,
  `needs_review`). The vault is the source of truth; Bases dashboards update automatically.
- Anything you author without explicit sign-off stays `needs_review: true`.
- After the sweep, run `mc standup --draft` so the day's plan reflects the cleaned state.

## When to run

Weekly (Sunday is the documented cadence), or whenever the Needs-Review count or overdue
pile has grown. This is collaborative — the user decides; you prepare and propose. Not scheduled
(unlike the 6:45am `harvest`/`standup`), because it needs the user in the loop.

Engine: `~/mission-control/bin/weekly.py` · design: `~/mission-control/README.md`.
