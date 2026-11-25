---
name: explain
description: Read-only orientation to the current branch/plan — always shows a simple explanation, what's decided, an example (when applicable), and how it fits the architecture + files, then offers numbered drill-downs into specifics (incl. an optional /teach lesson). Built to run in a fresh session beside your main one; never writes files.
---

# Explain

Stand-alone, **read-only** walkthrough of whatever the current branch is doing. Built to run in a **fresh session in parallel** to your working session: you keep coding in the main one, you read and ask questions here. Reuses `/teach`'s pedagogy. The shape is **core then questions** — a standing overview every run, then numbered drill-downs into concrete specifics.

## Hard constraint — never writes

No `Write` / `Edit`, no file creation, no commits, no builds, no git mutations. **Read + discuss only.** Read-only git inspection (`git log`, `git diff`, `git branch`) is fine. If asked to change code, decline and point to the main session. Single exception: an explicit user demand to write something ("save this to `docs/…`") — confirm the path, then write only that.

## Input

> $ARGUMENTS

Optional focus. Empty → explain the **current branch's** work. A topic / path / module → explain that instead.

## Phase 1 — Gather (read-only)

1. **Intent** — `git branch --show-current`, `git log main..HEAD --oneline`, `git diff` (working tree), `git diff main...HEAD --stat`.
2. **The plan** — Glob `plans/*.md`; read the one matching the branch (keywords / recency). No plan? Derive intent from commits + diff and say so.
3. **Architecture** — `CLAUDE.md` + the `docs/` it points to for the touched area; `.claude/rules/` for constraints in play.
4. **Pitch** — read `~/.claude/skills/teach/learner-profile.md` and pitch to that background; use analogies only where they genuinely clarify.
5. **Breadth (optional)** — large/unfamiliar area → fan out 2-3 `model: "sonnet"` sub-agents per `/study` Phase 2.

## Phase 2 — Overview (always shown)

The standing picture — render these every run, each tight, in order:

- **Explanation (simple)** — the goal in plain language, where we are against the plan (done / doing / next), and the one "if you remember one thing…" mental model.
- **What's decided** — the key choices already taken on this branch, and what was rejected.
- **Example(s)** — *when applicable*, walk one representative type / flow / change end-to-end, with paths + line numbers. Skip if there's nothing concrete to walk.
- **Architecture fit** — where the work sits in the layering / Core Principles, and which existing pattern it follows (cite files).
- **File fit** — a simple map (short tree or `A → B` arrows) of the main files involved and how they connect; reads as a pair with architecture fit.

## Phase 3 — Follow up (numbered drill-downs, read-only loop)

After the overview, offer the drill-downs as a **spaced, plain-prose numbered list** — give each item room to breathe; **don't** wrap it in a code fence (it cramps the text) and **don't** use `AskUserQuestion`. Up to 9 items, but **only as many as genuinely apply — never pad to reach 9.** Each is 1-2 sentences naming a real, specific thing from *this* branch, spread across whichever dimensions fit:

- a deeper **architecture** aspect
- a concrete **issue / edge case / risk** in the current work
- a **design decision** + its trade-off (and what was rejected)
- a **rendering-pipeline / under-the-hood** concept the work leans on — how it actually works down low
- a **technical deep-dive** — a transferable web / system concept it touches (runs as a `/teach` Mode-1 lesson)
- a specific **file / type / flow** connection

Render it spaced, e.g.:

1. **The plan deviation** — why the no-cube branch deliberately keeps the override instead of clearing it, and whether that's actually safe.

2. **Last-applied diffing** — how the new tracking field fixes the missed alignment-default flip, and the sibling fields it mirrors.

Close with: *Pick any (e.g. `1, 3`), or ask anything specific — `Q` to finish.* Expand each pick in depth (paths + lines), then offer a fresh spaced list. Stay in explain mode (read-only) until done.

- A **technical-deep-dive** pick runs as a `/teach` lesson; skip its learner-profile write unless they ask to track it.

## Does NOT

Plan, implement, refactor, commit, build, or write artifacts. For any of those, switch to the main session. This skill only reads and explains.
