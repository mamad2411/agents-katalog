---
name: standard-development
description: |
  Standard development path for feature additions, API extensions, new
  components built on top of an existing codebase, and any brownfield
  change that is too large for /quick-development but does not require
  a full architectural overhaul.

  AUTO-FIRE immediately when the user says any of:
  - "add a feature", "build this feature", "implement [X]"
  - "extend [component/API/module]", "add [X] to existing [Y]"
  - "standard development", "/standard-development [description]"
  - escalated from /quick-development (scope exceeded threshold)

  Use when: 3–8 implementation tasks, touches 5–15 files, 2–4 phases.
  Do NOT use for large architectural overhauls or multi-system rewrites —
  use /full-development. Do NOT use for new greenfield products — use
  /new-development.
---

# Standard Development

Read ~/.claude/skills/shared/context-guardian.md now and apply all rules
within it for the entire session before doing anything else.

---

## Step 1 — CONTEXT.md check

Look for CONTEXT.md in the project root.

**If CONTEXT.md does not exist:**
Proceed to Step 2 (grill-with-docs full 5Q session).

**If CONTEXT.md exists and was modified within the last 30 days:**
```
CONTEXT.md found (last updated: [date] — current).
Loading domain language. Skipping grill-with-docs.
```
Load CONTEXT.md. Proceed to Step 3 (GSD evaluation).

**If CONTEXT.md exists but was last modified more than 30 days ago:**
```
CONTEXT.md found but may be stale (last updated: [date]).
Running a 3-question refresh to verify domain language is current.
```
Proceed to Step 2 with a 3-question cap (not 5).

---

## Step 2 — grill-with-docs (domain alignment)

Invoke the grill-with-docs skill from mattpocock/skills.

**Standard run (no CONTEXT.md): 5 questions maximum.**
**Refresh run (stale CONTEXT.md): 3 questions maximum.**

The grilling session:
- Reads the existing codebase to find ambiguous or inconsistently used terms
- Challenges the user's plan against the existing domain model
- Asks one question at a time, waits for response before continuing
- Updates CONTEXT.md inline as terms are resolved
- Creates an ADR entry only when all three are true:
  hard to reverse + surprising without context + result of a real trade-off

At the end of the session, confirm:
```
CONTEXT.md updated. Domain language locked for this session.
Terms locked: [list key terms and their definitions]
Proceeding to phase planning.
```

Use Opus for this step. Switch to Sonnet for all subsequent steps.

---

## Step 3 — GSD evaluation

Estimate the task scope:

Count the distinct implementation tasks required.
Count the files that will be touched.

**If fewer than 3 phases are needed AND the work fits under 40% context:**
```
Task fits in a single session. Skipping GSD.
Using Superpowers /write-plan directly.
```
Skip to Step 4B (direct Superpowers execution).

**If 3 or more phases are needed OR the work will not fit in one session:**
```
Task requires [N] phases. Invoking GSD for phase planning.
```
Proceed to Step 4A (GSD path).

---

## Step 4A — GSD path (3+ phases)

**Invoke GSD /gsd-plan-phase.**

Before presenting the plan to the user, run GSD phase pre-validation
as defined in context-guardian.md:
- Estimate token consumption per phase
- Split any phase exceeding 80k tokens
- Present the revised plan

GSD plan presentation:
```
Phase plan ready:
  Phase 1: [name] — [N] tasks — estimated [Xk] tokens
  Phase 2: [name] — [N] tasks — estimated [Xk] tokens
  ...
  Total: [N] phases — [Xk] tokens midpoint across sessions

Approve this plan? YES to proceed / REVISE to adjust
```

Wait for approval. Do not execute without explicit YES.

**After approval — Ralph Loop evaluation:**

Read ~/.claude/skills/shared/ralph-loop-gate.md.
Present the Ralph gate (phases × 50k midpoint formula).
Wait for YES (autonomous) or NO (manual).

Execute phases per the user's choice using Superpowers TDD (Step 5).

---

## Step 4B — Direct Superpowers path (1–2 phases, single session)

Invoke Superpowers /write-plan:
- Break the feature into tasks with exact file paths and verification steps
- Present the plan for approval before execution

```
Implementation plan:
  Task 1: [description] — [file path]
  Task 2: [description] — [file path]
  ...
Approve? YES to execute / REVISE to adjust
```

Wait for approval. Then invoke Superpowers /execute-plan.

---

## Step 5 — Superpowers TDD execution (applies to both paths)

For every task, without exception:

1. **RED**: write the failing test first. Confirm it fails.
2. **GREEN**: write the minimal implementation that makes the test pass.
3. **REFACTOR**: clean up without changing behaviour.
4. Commit after each task with a descriptive message.

Superpowers /code-review runs after all tasks in a phase are complete
(two-stage review: spec compliance, then code quality).

If critical or high issues are found: fix before moving to the next phase.
Do not carry blocking issues forward.

---

## Step 6 — Full delivery gate

Read ~/.claude/skills/shared/delivery-gate.md — Variant B (Full).

Run both review steps in sequence:
1. Superpowers /code-review (spec + quality)
2. G Stack /review (security + completeness + architecture)

Do not create a PR until the gate returns PASS.

Add G Stack /qa only if UI changes were made (see delivery-gate.md rules).

---

## Token budget

Target: 55k–80k tokens for the full session (or per phase if multi-phase).
GSD path: expect 80k tokens across sessions.
Single-session path: target under 60k tokens (within safe zone).
Model routing: Opus for grill-with-docs. Sonnet for all execution.
Context guardian hard stop at 50% applies in every session.
