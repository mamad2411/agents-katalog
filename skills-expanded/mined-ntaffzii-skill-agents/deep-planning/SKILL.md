---
name: deep-planning
description: Use this skill for any non-trivial coding task — new features, multi-file changes, architecture decisions, bug fixes with unclear root cause, or any request where the "obvious" first solution might not be the best one. Do NOT use for mechanical tasks (typo fixes, formatting, adding a single import, renaming a variable) — those should stay in Fast Mode.
---

# Deep Planning

You are operating in a mode designed to emulate careful, senior-engineer-level reasoning
(similar to how Claude Opus 5 approaches ambiguous engineering tasks) rather than
executing the first plan that comes to mind.

## Core rule

**Never start editing code as your first action on a task this skill applies to.**
Your first output must always be a structured Implementation Plan artifact
(see format below), and you must wait for explicit approval ("Proceed") before
writing or modifying any file.

## Step 1 — Restate and question the request

Before proposing any solution:
- Restate the task in your own words in 1-2 sentences.
- List every assumption you are making. If the request is ambiguous on scope,
  data shape, error handling, or edge cases — say so explicitly instead of
  silently picking one interpretation.
- If a genuinely blocking ambiguity exists (the plan would differ significantly
  depending on the answer), ask ONE clarifying question before proceeding.
  Otherwise, state your assumption and continue — do not stall on minor ambiguity.

## Step 2 — Read before you write

- Search the existing codebase for related code, existing conventions, naming
  patterns, and prior art before proposing anything new. Do not assume a greenfield
  solution if similar logic already exists elsewhere in the repo.
- If there is an existing Implementation Plan artifact for this feature/thread,
  **read and extend it — never silently replace it.** Diff your new plan against
  the old one and call out explicitly what changed and why. If the user's new
  instruction only affects part of the plan, keep the untouched sections intact.

## Step 3 — Generate at least two real approaches

For any design decision that has more than one reasonable solution, briefly outline
at least 2 options (not one option plus a strawman). For each option, note:
- What it optimizes for
- The main tradeoff or risk
- Rough implementation cost (small / medium / large)

Pick one and state *why*, in one sentence. Skip this step only for tasks with
a single obviously correct implementation (e.g. "add a null check here").

## Step 4 — Surface edge cases and failure modes

Before finalizing the plan, list:
- Inputs or states that could break the chosen approach
- Anything the change could silently affect elsewhere in the codebase
  (shared functions, callers, tests, config)
- What "done" looks like — how you (or the user) will verify correctness

## Step 5 — Write the Implementation Plan artifact

Structure every plan artifact the same way, so it stays diffable across revisions:

```markdown
## Goal
<one sentence>

## Assumptions
- ...

## Options considered
1. **<name>** — optimizes for X, tradeoff: Y, cost: small/medium/large
2. **<name>** — optimizes for X, tradeoff: Y, cost: small/medium/large

## Chosen approach
<option> — because <reason>

## Steps
1. ...
2. ...

## Risks / edge cases
- ...

## Verification
- ...
```

Stop and wait for the user to comment on or approve this artifact before touching any files.
If the user replies in chat instead of commenting on the artifact directly, treat that
reply as feedback on the **existing** artifact and update it in place — do not generate
a competing new plan.

## Step 6 — Handoff to execution

Once the plan is approved, execution (including fast, mechanical edits) can proceed
under a faster model if the workflow uses a separate implementer agent — this skill only
governs the *planning* phase. See `architect.md` / `implementer.md` custom agents for
a model-routing setup that pairs with this skill.
