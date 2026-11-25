---
name: handoff
description: Session lifecycle -- "/handoff start" (session briefing), "/handoff wrap" (update handoff.md + local commit), "/handoff save" (emergency snapshot), "/handoff docs" (checkpoint: update handoff.md, no commit)
---

# Handoff -- session lifecycle (v3)

One skill, four subcommands. Detect the mode from the argument: `start`, `wrap`, `save`, `docs`. No argument -> reply with one usage line listing the four modes and stop.

## CONFIG (all modes)

- Output language: English. No emojis in docs.
- Repo mode: single repo at project root (branch `main`).
- Files (project root): `handoff.md` (live state -- HARD CAP ~120 lines, max 2 session sections, Session Summary max 10 rows, Key Files max 10 rows), `handoff-archive.md` (overflow, newest first -- NEVER read during start), `emergency-snapshot.md` (fire exit).
- Wrap is AUTOMATIC: update handoff.md, rotate overflow, commit locally -- no confirmations. NEVER push without an explicit user request.
- AUTO-WRAP RULE (two rungs, they ask for different things): at ~20% the Stop hook asks for a CHECKPOINT -- run `docs` (update handoff.md, no commit) and KEEP WORKING, the session does not end. At ~22% it asks for the full `wrap` -- stop new work and end the session. Act on either unasked; the same applies if you independently notice context getting long.
- If CLAUDE.md defines project-specific "Handoff extras" (e.g. a wiki/vault sync), honor them during wrap.

## Token discipline (the point of this design)

- start reads ONLY `handoff.md` (+ the snapshot if present). Never the archive, knowledge folders, or CLAUDE.md (auto-loaded).
- Need history mid-session? Read `handoff-archive.md` at that moment, never preemptively.
- Record in handoff.md only what git CANNOT tell a future session: decisions, rejected approaches and why, gotchas, open questions. Never re-list changed files or restate commit messages.

## Mode: start

Read-only (exceptions: delete a consumed snapshot; the fast-forward pull in step 2).

1. Repo state FIRST, handoff second. If `scripts/session-status.sh` exists, run `bash scripts/session-status.sh` (it fetches itself and prints a pull verdict). Otherwise run `git fetch origin` first (skip if no remote), then in parallel: `git status -sb`, `git log --oneline -5`, `git rev-list HEAD..@{u} --count` (behind), `git rev-list @{u}..HEAD --count` (ahead). No upstream or error -> treat both as 0 and note "local-only"; no `.git/` -> skip git, note it. **Do NOT read `handoff.md` yet if behind > 0** -- a parallel machine may have wrapped a session you don't have.
2. Reconcile BEFORE trusting handoff (the cross-machine fix: detect-and-reconcile, never brief from a stale working-tree handoff when origin is ahead):
   - **behind > 0, ahead = 0, tree clean** -> `git pull --ff-only` now (lossless), then read `handoff.md`.
   - **DIVERGED (ahead > 0 and behind > 0) or behind + tree dirty** -> do NOT pull. Brief from origin's copy via `git show @{u}:handoff.md` and flag the divergence / uncommitted work in Heads Up for the human to reconcile.
   - **behind = 0 / local-only** -> read `handoff.md` normally.
3. If `emergency-snapshot.md` exists: read it, fold it into the briefing, delete it after presenting (it is consumed).
4. Present the briefing, max ~25 lines total:

```
## Session Briefing
**Last session:** <N> -- <title from handoff.md>

### Repo Status
| Branch | Status | Unpushed | Last commit |

### What To Do Next (top 5)
<top 5 rows of the handoff table; flag rows that look already done per git log>

### Emergency Recovery (only if snapshot existed -- max 5 lines)

### Heads Up
<uncommitted/unpushed work, stale items; handoff.md over ~150 lines means the
last rotation failed -- flag it and offer to rotate now.
If step 2 fast-forwarded: "Pulled N commits from origin (fast-forward)."
If DIVERGED or behind+dirty: "Local and origin diverged / uncommitted work --
briefed from origin's handoff; reconcile before committing."
Else: "All clear.">
```

- If `handoff.md` is missing: say so and suggest `/handoff wrap` to create it from the template below.

## Mode: wrap

ORDER MATTERS: documentation is updated BEFORE the commit, so the wrap commit includes the handoff it wrote and the repo is left clean.

1. Assess: `git fetch origin` first (skip if no remote), then in parallel: `git status -sb`, `git diff --stat`, `git rev-list HEAD..@{u} --count` (behind), `git rev-list @{u}..HEAD --count` (ahead). Skip re-reading handoff.md if it is already in context this session -- UNLESS behind > 0: another machine may have wrapped a session since, so reconcile before writing a session row on stale numbering:
   - **behind > 0, ahead = 0, tree state permitting** -> `git pull --ff-only` (stash/restore local edits around it if needed), then re-read `handoff.md` -- session N and the tables come from the pulled version.
   - **DIVERGED or pull impossible** -> do NOT pull. Read origin's copy (`git show @{u}:handoff.md`), take session numbering and table state from WHICHEVER is fresher, write the update on top of the local file, and flag the divergence in the report -- the human reconciles before push.
2. Update `handoff.md` automatically:
   - Same-session idempotency: if a "What Was Done (Session N)" section for THIS working session already exists (e.g. an auto-wrap ran earlier in this chat), UPDATE it in place -- never create a duplicate. Otherwise N = last Session Summary row + 1.
   - New section goes BEFORE "What To Do Next": `## What Was Done (Session N) -- <short title>` with terse bullets, max 8. Convert relative dates to absolute.
   - Refresh: Current State; What To Do Next (drop completed rows); Key Files only if a file matters for the NEXT steps (prune to max 10 rows); this session's Session Summary row.
   - Unfinished work is the whole point: every task still in flight goes into What To Do Next as RESUMABLE state -- what is done, what remains, and the exact file/branch/command to pick up. A row that only says "continue X" has thrown away the context that made it cheap to resume.
   - Touch CLAUDE.md only if the project phase or strategy genuinely changed (rare).
3. Rotate overflow: if more than 2 session sections OR over ~120 lines, move the oldest "What Was Done" sections to `handoff-archive.md` (newest at TOP, under heading `# Handoff Archive (do not read on /start)`; create the file on first rotation; append-only -- never trim it). Session Summary over 10 rows -> move oldest rows to the archive's own table.
4. Commit locally: review `git status` briefly, then `git add -A` and commit with a descriptive message. Leave out junk or abandoned experiments and mention them. Do NOT push.
5. Report, max 10 lines: commit hash + message, what "What To Do Next" now says, rotation yes/no, warnings. No questions. If everything was already clean and current: "All wrapped. Nothing to do."

## Mode: save

Fire exit -- max 6 tool calls, no commit, no reads except `git status -sb`. Write from what is already in context, fast, then stop. Create/overwrite `emergency-snapshot.md`:

```markdown
# Emergency Snapshot -- Session <N>
Date: <today>

## What was done this session
## Uncommitted work            <- from git status, or "all clean"
## Key context                 <- root causes, decisions, gotchas that would otherwise be lost
## Next step when resuming
```

`/handoff start` consumes and deletes this file next session.

## Mode: docs

Checkpoint mode -- this is what the ~20% auto-wrap nudge asks for. Run wrap steps 2-3 only (update + rotate), no commit, then CONTINUE working; docs never ends the session. Same same-session idempotency rule as wrap: if this session's "What Was Done" section already exists, update it in place.

## handoff.md template (first wrap, if the file is missing)

```markdown
# <Project> -- Handoff

<!-- HARD CAP ~120 lines. Max 2 session sections. Overflow -> handoff-archive.md -->

## Current State

- **Phase:** <phase>
- **Session count:** <N>
- **Repo status:** <status>

## What Was Done (Session N) -- <short title>

- <bullet>

## What To Do Next

| # | Priority | Task |
|---|----------|------|
| 1 | High | <task> |

## Key Files

| File | Purpose |
|------|---------|
| `handoff.md` | Current state + next steps (capped; history in handoff-archive.md) |

## Session Summary

| Session | Date | Title |
|---------|------|-------|
| 1 | <date> | <title> |
```
