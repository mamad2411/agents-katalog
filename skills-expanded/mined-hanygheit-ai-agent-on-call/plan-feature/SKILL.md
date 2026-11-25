---
name: plan-feature
description: Turn a ticket into an approved plan before any code is written. Use when starting any non-trivial feature, bug fix or refactor, or when the user says "plan", "spec", or gives a ticket ID. Writes docs/specs/<ticket>.md and stops for human approval.
---

# Plan a feature (Rules 02 + 03: outcome, plan, approval — then code)

You are writing a plan, not code. Do **not** edit source files in this skill.

## Steps

1. **Get the outcome.** If the request is only a command ("add retries"), ask for
   the goal, non-goals, constraints and acceptance test before planning. One short
   question at a time.
2. **Read before you plan.**
   - `AGENTS.md` (team rules) and any relevant `docs/adr/*.md`
   - `docs/runbooks/` if the change touches production behaviour
   - Search for every caller of the code you will change.
3. **Write the plan** to `docs/specs/<TICKET>.md` using `docs/specs/_TEMPLATE.md`.
   Keep it short: outcome, approach, files to touch, tests, rollback, open questions.
4. **Size check.** If the plan touches more than ~3 files or ~200 lines, propose
   splitting it into smaller tickets instead.
5. **Stop.** End with:
   `Plan written to docs/specs/<TICKET>.md — waiting for your approval before changing any code.`
   List open questions explicitly. Never answer your own open questions by guessing.

## After approval (only when the human says so)

- Work on branch `agent/<ticket>-<slug>` (never `main`), ideally in its own worktree.
- Implement exactly the approved plan. If scope grows, stop and update the plan first.
- Tests with every change. Open a **draft PR** that links the spec.
