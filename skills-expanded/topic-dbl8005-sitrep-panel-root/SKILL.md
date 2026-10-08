---
name: sitrep-panel
description: |
  Keep a live local HTML report updated as you work on a task — a status
  board, a running "what's happening now" narrative, screenshots, and a
  newest-first log — served on localhost so the user can watch progress in
  a browser tab instead of reading the transcript. Use when the user invokes
  /sitrep-panel, asks for a "progress report", "status page", "live doc",
  or wants visibility into a multi-step task as it happens.
license: MIT
metadata:
  version: "1.1.0"
---

# sitrep-panel

A live local HTML report you keep updated as you work. It lives at
`.sitrep-panel/report/` inside whatever project you invoke it from, served
on localhost, and it live-reloads in the browser every time you update it —
the user never has to hit refresh.

This is explicitly **not** a Claude Artifact. It never leaves the user's
machine, needs no publish step, and works offline. Use it whenever the user
wants to *watch* a task happen rather than read about it after the fact.

## Invocation

`/sitrep-panel [start | open | stop | archive]` — default (no argument) is
`start`.

- **`start`** (default) — scaffold a new report if none is active, or resume
  the active one. Always ends by printing the localhost URL prominently.
- **`open`** — just print the URL of the active report (start the server if
  it isn't running); never touches content.
- **`archive`** — move the current active report to
  `.sitrep-panel/archive/<timestamp>-<slug>/` and scaffold a fresh one. Use
  this when starting genuinely new, unrelated work rather than continuing
  the current task.
- **`stop`** — kill the background server. Content on disk is untouched;
  `start` or `open` later brings it back.

## First run — scaffold

If `.sitrep-panel/report/` doesn't exist yet in the current project:

1. Create `.sitrep-panel/report/screenshots/`.
2. Copy `assets/template.html` (from this skill's own directory) to
   `.sitrep-panel/report/index.html`. Replace `{{TITLE}}` with a short name
   for the task, and `{{SUBTITLE}}` with one line of context (what this
   report is tracking, and when it started).
3. Write `.sitrep-panel/report/meta.json`:
   ```json
   {"updated_at": "<current ISO-8601 UTC timestamp>"}
   ```
4. If the project is a git repo and `.sitrep-panel/` is not already covered
   by `.gitignore`, append it (`echo '.sitrep-panel/' >> .gitignore`) — this
   is local scratch, not something to commit. Mention you did this; don't
   ask first, it's trivially reversible. If the user tells you they want
   report history committed instead, skip this step and say so.

If `.sitrep-panel/report/` **already exists**, skip scaffolding — resume it.
Use `archive` first if this is unrelated new work and you want a clean slate.

## Serving it

Start the bundled server in the background, from this skill's own directory
(so the relative path to `scripts/serve.py` resolves regardless of the
user's cwd):

```bash
python3 <this-skill-dir>/scripts/serve.py <project>/.sitrep-panel/report
```

Run this with your background-execution mechanism (e.g. the Bash tool's
`run_in_background: true`) — it blocks forever. It prints exactly one line,
`SERVING http://localhost:<port>/`, before blocking; capture that line for
the URL. It auto-picks a free port (tries 8934 first, falls back to any free
port on conflict), so it's safe to have several reports running for
different projects at once.

Record the port for reuse: write `.sitrep-panel/report/.server.json`
(`{"port": <port>, "started_at": "<iso8601>"}`) right after start, gitignored
along with the rest of `.sitrep-panel/`. On a later `start`/`open` in the
same or a resumed session, read this file first — if a `GET` to
`http://localhost:<port>/meta.json` succeeds, the server is already up,
reuse that URL instead of spawning a second one.

**Always tell the user the URL after `start` or `open`, even if you just
reused an existing server.** This is the whole point of the skill — don't
bury it in a paragraph.

## The update protocol — what makes this useful

This is the part that matters. A sitrep-panel that only gets written once at
the start is worthless. Update it at every real step, not just at the end:

1. **Update "What's happening now"** (`#current-work-body`) with prose — what
   you're doing right now and *why*, not just a status word. Replace the
   whole block's content each time; this section always reflects the
   present, not history.
2. **Prepend a new log entry** to `#entries` (newest-first — insert right
   after the `<div id="entries">` opening tag, before whatever was already
   there), using the exact `.entry` / `.entry-rail` / `.entry-dot` markup
   shown in the template's commented example — the timeline rail depends on
   that structure. One entry per real step: what happened, what you decided
   and why, what you verified. Skip entries for trivial reads; log entries
   for writes, decisions, and verification results.
3. **Save screenshots** into `.sitrep-panel/report/screenshots/` and
   reference them with a relative `<img src="screenshots/whatever.png">` —
   either inline in a log entry, or appended to `#shots-body` (or both, when
   a screenshot is the standout evidence for a step).
4. **Update the board** — the board is four columns, each with its own
   container: `#board-todo`, `#board-progress`, `#board-done`,
   `#board-blocked`. Add/move/remove a plain `<div class="board-card">…</div>`
   in the container matching its current status as steps start, block, or
   finish — moving a card means removing it from one column's container and
   appending it to another's, not changing a class. See the commented
   example markup in the template.
5. **Touch `meta.json` last, always.** Rewrite `updated_at` to the current
   ISO-8601 UTC timestamp as the final write of every update — the page
   polls this file every 2s and reloads on change, so writing it before the
   content write would show a stale reload. This is the one step you must
   never skip.

## Tracker-synced board (optional)

If the project has a working issue tracker connection available to you right
now (an already-connected Atlassian/Jira MCP, `gh issue list` for a GitHub
repo, a connected Linear MCP, etc.) **and** there are real tickets relevant
to this task, render the board from that real data — real ticket key, real
title, real link, real status mapped to the matching column. Refresh it
each time you update the doc, the same as everything else.

If no tracker is connected, or nothing relevant is filed there, fall back to
a plain manually-maintained checklist — steps you define yourself, kept in
sync by hand. **Never fabricate ticket data to fill the board**, and don't
silently guess which tracker to use — if more than one is plausible, ask.

## Notes

- One active report per project at a time by design (`.sitrep-panel/report/`
  is a fixed path) — this keeps the URL stable across a whole session
  instead of minting a new one per task. Use `archive` to start clean.
- The report is genuinely static HTML plus polling JS — no build step, no
  external requests, works with the browser fully offline once loaded.
- If the user asks for a report shareable with people who aren't at their
  machine, that's a Claude Artifact, not this — tell them so; this skill is
  specifically for local/private, zero-publish visibility.
