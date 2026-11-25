---
name: save
description: Reconcile project state before a break, or capture an out-of-band note into the right memory surface. Routes to one branch and runs only that one.
disable-model-invocation: true
---

# familiar — Save

A **menu, not a procedure**. It names the two ways durable state gets written outside a formal
check-in and hands off to exactly one of them. It reads no project state itself and writes
nothing.

## Context contract

- **Required context:** this menu only
- **Conditional context:** exactly one file under `references/`, only when step 1 selects that branch. The selected branch's own context contract governs from that point; nothing else in `references/` is opened.
- **Excluded context:** `5-System/Memory/`, `4-Trackers/`, `Knowledge`, `Inputs`, other projects, and undeclared extension content — the menu itself opens no project content.
- **Updates:** `nothing`. Every write belongs to the selected branch and is declared in that branch's own contract
- **Capabilities:** file-read. Optional capabilities must degrade as the procedure states.
- **Completion:** One branch is selected, its reference file is loaded, and its procedure runs under its own contract — or the user is told no branch fits and nothing is opened.

## Step 1 — Select the branch

If the user already named one ("I'm heading out", "remember this", "log this decision") — including
by argument, `/save progress` or `/save to-memory` — skip the question and go straight to it.
Otherwise present these two and ask which:

| Branch | Reference | What it does |
|---|---|---|
| **Save progress** | `references/progress.md` | Reconcile project state before the user steps away, logging loose ends across every track without creating a new state file. |
| **To memory** | `references/to-memory.md` | Capture one out-of-band note, or add, edit, complete, or reschedule a single task — a decision, task change, risk, or preference — into the right memory surface. |

If the request matches neither, say so and stop. Do not pick the nearest branch, and do not open a
reference file to find out whether it fits — the table above is the whole basis for the match.

## Step 2 — Run the selected branch

Load that one reference file. From there its own **Context contract** governs — its Required,
Conditional, Excluded, Updates, Capabilities, and Completion declarations replace this file's, which
covered only the menu. Do not load a second branch.

## Guardrails

- **Every branch here is user-started.** This skill carries `disable-model-invocation: true`, so a
  route match never opens it and never opens anything under `references/` — `routes.md` Resolution
  rule 3 applies to the menu, which is what keeps it applying to both branches. Identify the branch
  that fits, tell the user the command, and stop.
- The menu never performs a branch's work itself, never partially applies one, and never substitutes
  a lighter action because a branch looked heavy.
- Nothing under `references/` is a skill. Each is a procedure this menu selects; none is separately
  invocable, and none may be opened without a selection in step 1.
