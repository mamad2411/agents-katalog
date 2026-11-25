---
name: project-docs
description: Use when entering an unfamiliar project, when creating or repairing a project's agent docs (AGENTS.md, feature map, lat.md folder map, VISION.md, ES.md), or when the workspace check reports doc problems.
---

# Project docs

Each fact about a project has one home. Read in this order: `AGENTS.md` (loaded already), `ES.md`, then the feature file for the task. Use the folder map before you add a file and `VISION.md` when scope is in question. A README supplements these files; it never replaces them.

## One file per job

| File | Holds | Limit |
| --- | --- | --- |
| `AGENTS.md` (+ `CLAUDE.md` = `@AGENTS.md`) | `## Start here` (pointers), `## Common mistakes` (this project's lessons), `## Rules` | 60 lines |
| `ES.md`, title "(updated YYYY-MM-DD)" | `## Now`, `## Next`, `## Broken`, `## Open decisions` | 40 lines |
| `VISION.md` | identity in one line, `## Thesis`, `## Non-goals` | 25 lines |
| `lat.md/workspace.md` | every top-level item and why it exists | — |
| `.agents/skills/verify-<app>/features/` | one file per user-facing feature: how to reach it, drive it, its code, its gotchas; made by `create-verification-skill`, kept true by `maintain-verification-skill` | — |
| `reports/`, commit messages | evidence: hashes, run IDs, verification prose | — |

A workspace check can enforce the limits and headings (here: `findability/check_pointers.py`). These files are local notes: keep them out of public git and link them into new worktrees.

## What goes in AGENTS.md

It loads into every session, so each line must apply to every task there (HumanLayer, *Writing a Good CLAUDE.md*; Anthropic, *Steering Claude Code*).

- Yes: what the project is, how to build, test and verify it, where things live (as pointers), and rules that hold for every task.
- No: procedures (a skill), task-specific notes (the feature file), state (`ES.md`), copies of global rules (the user-level instructions), code style (a linter).
- A "never do X" that agents keep breaking needs a check or hook; the line in `AGENTS.md` is not enough.
- A common mistake is one dated line: what went wrong, the rule, and its guard (or "No guard").

## What goes in ES.md

- `## Now`: what is true today, in up to five lines. Each line states a fact; its proof goes to `reports/`.
- `## Next`: the user's open requests, newest date first, one line each, starting `Feature:`, `Fix:`, `Remove:` or `Keep:`. Delete a line only when the user has seen it working. When the log outgrows the file, it moves to a local `REQUESTS.md` beside `ES.md` (same line format), and `## Next` keeps the user's ranked items and a link.
- `## Broken` and `## Open decisions`: one line each; a decision names who decides.
- Rewrite the file in place; never append a progress log.

## Keep them true

- Change a fact in its home only; elsewhere, point to it.
- When a doc contradicts the code or another doc, check the code, fix or delete the wrong text, and say what changed.
- Before you delete old text, move each lesson or prohibition that is still valid to a feature's gotchas or to `AGENTS.md`.
- Add a harness part (`init.sh`, a rubric, a lint) only for a workflow that repeats, and only the smallest that fixes the bottleneck. If you are not sure it is still needed, remove it and keep the simpler setup if quality holds.

## Create the layout when absent

Inspect the project two levels deep, draft the missing files in the shape above, and show the user `VISION.md` before you save it. Exemplar: this library's `VISION.md`.
