---
name: resume-session
description: Load the most recent session file and re-establish context at the start of a new session. Use when continuing multi-session work. Pairs with /save-session.
---

# /resume-session — pick up where you left off

Goal: restore working context cheaply, without re-exploring.

## Do this
1. **Read the STATE spine first** — `.claude/STATE.md` (schema:
   `docs/state-and-artifacts.md`). Its frontmatter gives the machine-navigable position in
   one read: `phase`, `status`, `slug`, `next_skill`. If a `slug` is set, glance at
   `.claude/planning/<slug>/` (`SPEC.md` / `PLAN.md` / `VERIFICATION.md`) for the current
   artifacts. If STATE.md is absent, skip to the session file — the spine is optional.
2. Find the latest **session narrative** for the human story:
   - `.claude/sessions/` in the repo, else `~/.claude/harness-claude/sessions/`.
   - Pick the most recent by date; offer the user the last few if several exist.
3. Read it and **restate**: the objective, what's verified-working, what failed (avoid
   repeating those dead ends), and the concrete next steps.
4. Re-orient against current reality: confirm the repo state still matches (branch, key
   files). **If STATE.md and the session narrative disagree** (e.g. `next_skill` says
   `/harness-claude:implement` but the narrative describes shipping), **flag the drift and reconcile from
   the repo** — do not trust either blindly.
5. Propose the immediate next action (prefer STATE's `next_skill`, cross-checked against
   the narrative's "remaining"), and confirm with the user.

## Note
The SessionStart hook already surfaces STATE's `next_skill` (or a pointer to the latest
session file) automatically; this skill is the full, deliberate restore. Treat every file
as *what was true when written* — verify before trusting specifics (files/flags may have
changed).
