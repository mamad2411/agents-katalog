---
name: plan-task
description: >-
  Plan the implementation of a defined task before writing code. Trigger on
  "plan this out", "plan this", or before starting any multi-file change. Produces
  the file-level plan, risks, and verification strategy, grounded in the
  actual code (not assumptions).
---

# Plan task

## Steps

0. **Read the standard**: `engineering-standards` is the list the code will be
   marked against, so a plan that respects it costs nothing later.
1. **Read before planning**: locate every file the change touches (Grep/Glob),
   read the relevant parts. Never plan against an imagined codebase.
2. **File-level plan**: ordered list of edits, per file, with what changes and
   why. Call out shared contracts that must stay in sync across repos
   (e.g. the feature-column contract shared by serving and training).
3. **Behaviour events**: list the analytics events the change adds or changes,
   and which file emits each one. A new feature or a change to existing logic
   ships with its events in the same PR, never as a follow-up. If the plan has
   no events, say why in one line (pure refactor, nothing observable changed)
   instead of leaving it blank.
4. **Risks**: what can regress; which tests / LORO / manual flows gate the
   change. For model changes the gate is multi-season LORO, not noisy
   single-season deltas.
5. **Verification strategy**: exact commands to prove it works end-to-end
   (tests with the project's CI --ignore set, curl of the real endpoint,
   running the app), not just typecheck.
6. Keep the plan proportional: a one-file fix needs three lines, not a
   document.
