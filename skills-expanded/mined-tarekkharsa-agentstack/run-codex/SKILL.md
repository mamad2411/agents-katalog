---
name: run-codex
description: Delegate clear-spec, bulk, or mechanical work — migrations, codemods, large refactors, log digs, and independent code review — to gpt-5.5 through the Codex CLI, with quota-aware fallback to Claude models.
---

# Run Codex (gpt-5.5)

Use this skill when you want to hand a well-specified chunk of work to gpt-5.5
(via OpenAI's Codex CLI) instead of doing it inline — because it's
bulk/mechanical, or because you want a second, independent perspective on
something that ships.

## When to reach for Codex

- **Bulk / mechanical work you can fully specify** — migrations, codemods,
  repetitive refactors, large data or log analysis.
- **An independent review** — a second opinion on a diff or plan, from a
  different model than the one that wrote it.
- **Not** for taste-critical UI/copy/API design, or vague tasks you can't pin
  down — those stay with the orchestrating model.

Rule of thumb: **if you can fully specify the task in the prompt, it's a good
Codex job.** If you can't specify it, don't delegate it.

## Commands

```bash
# Investigate / review — read-only, cannot edit files:
codex exec -s read-only "<self-contained prompt>"

# Make edits — can modify the working tree:
codex exec "<self-contained prompt>"

# Review a diff — scope is required (bare `codex review` errors):
codex review --base <branch>        # or --uncommitted, or --commit <sha>
```

## Write self-contained prompts

Codex starts fresh — it does **not** see your conversation. Every prompt must
carry its own context: the goal, the exact files/paths, the acceptance
criteria, and any conventions that matter.

**Codex reads `AGENTS.md`, not `CLAUDE.md`.** If the project's conventions live
in `CLAUDE.md` (build/test commands, style, commit format), paste the relevant
ones into the prompt.

## Timeouts

Codex runs can exceed a 10-minute command timeout. Pass an explicit longer
timeout, or run it in the background and poll for its output / report file.

## Parallel edits → isolate

If you run several editing Codex jobs at once, give each its own git worktree so
their edits don't collide in the shared checkout.

## Quota-aware fallback (important)

Codex access is usually a finite quota, not unlimited.

- On a **usage-limit / quota / 429** error: **do not retry** — quota errors
  don't clear by retrying. Redo the task with a Claude model instead
  (clear-spec/mechanical → a small model; tricky, user-facing, or review work →
  a strong model).
- Once Codex reports a limit, treat it as **exhausted for the session** — stop
  routing new work to it, and tell the user, so they know the token mix shifted.
- A **transient** failure (network, timeout, malformed output) is different: one
  retry is fine before falling back.

## Generate cheap, verify smart

A reliable pattern: let Codex (or any cheap model) produce the diff, then have a
stronger model review it. Reviewing costs a fraction of generating — so you get
bulk throughput without shipping unreviewed work.
