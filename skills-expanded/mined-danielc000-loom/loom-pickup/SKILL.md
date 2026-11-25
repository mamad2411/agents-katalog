---
name: loom-pickup
description: Use when resuming work or getting up to speed on a Loom task — "pickup", "continue", "what were we doing", "get back to". Reads the project board, recent git history, CLAUDE.md, and (if relevant) your living resume doc to brief the current state and a concrete next step.
---

# Pickup (Loom)

Get oriented in THIS project, then state a concrete next step. The session is already bound to its
repo and board — the **board is the source of truth for tasks**; the vault holds prose. Don't pass a
project id anywhere; it's derived server-side.

## Steps

1. **Board** — `tasks_list` (the `loom-tasks` MCP) to see tasks and their columns. Note what's
   in-progress, in review, and waiting, and surface which cards are **`held`** (an owner brake) vs
   **`deferred`** (not yet sequenced) so "what's next" respects them. Also drain the **Requests inbox**
   (`question_pull`) and check `escalation_status` for decisions the human answered while you were away.
2. **Code** — `git log --oneline -20` and `git status` for recent and in-flight work.
3. **Conventions** — read `CLAUDE.md` at the repo root if present.
4. **Your role's anchor** (whichever applies):
   - *Lead / orchestrator:* read your **living resume doc** — it's the "you are here + what's next"
     source of truth. Your session's **"Where things live"** context block already carries its resolved
     absolute path on the **`Resume doc:`** line, directly under **`Project vault dir:`**. **Read it from
     that exact `Resume doc:` line, verbatim — never construct or derive the path yourself** (there is no
     fixed `Projects/<Project>` segment under the vault dir, and the filename itself is a per-project
     override, so any hand-built path is likely wrong), **and never Glob, Bash `find`, or Bash `ls` for
     it either** (a broad search from your home directory hits the search timeout). Cross-check it
     against the board. **Before acting on a handoff's "still to build / un-built" claim, verify it
     against `git log`/`git merge-base` first** — work a resume doc calls unbuilt may already be merged on
     the mainline, and dispatching (or filing an owner go/no-go for) it re-derives work that already
     exists. If the injected `Project vault dir:` turns out wrong (the read 404s), don't fall back to a
     broad search — resolve the real vault root from Obsidian's own global config file (`obsidian.json`,
     under the OS's per-user app-data directory, e.g. `%APPDATA%\obsidian\obsidian.json` on Windows),
     which lists every known vault path; then retry against the resolved root.
   - *Worker:* your scope is your assigned board task / kickoff — orient narrowly to it, not the whole
     project.
5. **Design notes** (optional) — read **`_Index.md`** at the project vault root FIRST (the root is in
   your "Where things live" context block): it's the map-of-content that lists every note by group, so
   use it to locate the design/task notes you need **instead of Globbing or Bash `find`/`ls`** (a broad
   search from home times out). Notes live in a shallow, one-level taxonomy folder per the project's `CLAUDE.md` "Vault
   structure" section; fixed-path docs stay pinned at the vault root.
   - **If the owner says they edited or left notes in a file out-of-band**, force a fresh read of it: the
     harness `Read` "unchanged since last read" guard is arg-scoped (keyed off the last-read args, blind
     to an external edit) and can falsely return "unchanged" — vary the range (a different offset) so you
     pick up the owner's content, not a stale prior read.

## Brief

Summarize concisely — only what's needed to resume, not an exhaustive report:
- **What** the project is (one line).
- **In progress** — board state + any uncommitted work.
- **Decisions / gotchas** that bear on what's next (from the resume doc or notes).
- **Suggested next step** — one concrete action.
