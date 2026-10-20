---
name: full-development
description: |
  Full development path for large-scale brownfield work: major architectural
  overhauls, multi-system rewrites, large feature sets spanning 5 or more
  phases, and any brownfield change that requires a research phase before
  planning can begin.

  AUTO-FIRE immediately when the user says any of:
  - "full development", "/full-development [description]"
  - "major overhaul", "architectural change", "rewrite [module/system]"
  - "big change", "large implementation", "multi-phase build"
  - "refactor the entire [X]", "overhaul [X]"

  Use when: 5+ phases, 10+ files, architectural scope, existing codebase.
  Do NOT use for greenfield products that do not exist yet — use /new-development.
  If unsure: ask "Does a codebase for this already exist?" If no → /new-development.
---

# Full Development

Read ~/.claude/skills/shared/context-guardian.md now and apply all rules
within it for the entire session before doing anything else.

---

## Entry check — brownfield confirmation

Before doing anything, confirm the work is brownfield (existing codebase).

Ask: "Does an existing codebase for this already exist?"

**If YES:** Proceed to Step 1.

**If NO (no existing codebase):**
```
This sounds like a greenfield build — no existing codebase to extend.
/full-development is designed for large changes to existing code.
For new products, use /new-development which starts with G Stack
/office-hours to validate the idea before building.

Shall I route to /new-development? YES / NO
```
Wait for response. If YES, instruct the user to run /new-development
and carry forward the description they provided. Stop this session.
If NO, ask for clarification before proceeding.

---

## Step 1 — grill-with-docs (full, no question cap)

Invoke the grill-with-docs skill from mattpocock/skills.

No question cap for /full-development. The scope of work justifies
thorough domain alignment before any planning begins.

The grilling session runs until one of these is true:
- All significant ambiguous terms in the codebase have been resolved
- The user explicitly says "I think we have enough, let's proceed"
- 15 questions have been asked (absolute maximum — surface this to user)

The session:
- Reads the full codebase to surface domain language inconsistencies
- Challenges every assumption in the user's plan
- Locks terminology in CONTEXT.md with full definitions
- Creates ADRs for architectural decisions with genuine trade-offs

Check CONTEXT.md staleness first (same 30-day rule as /standard-development).
If CONTEXT.md is current: still run grill-with-docs but focus on the
specific scope of the overhaul, not the full domain.

```
CONTEXT.md status: [current / stale / not found]
Running grill-with-docs for [full scope / targeted refresh].
This may take 10–15 questions for a build of this size.
```

Use Opus for this step. Switch to Sonnet for all subsequent steps.

At completion:
```
Domain alignment complete.
CONTEXT.md updated with [N] new terms and [N] ADR entries.
Key decisions locked: [list]
Proceeding to GSD planning.
```

---

## Step 2 — GSD /gsd-new-project (always mandatory)

Invoke GSD /gsd-new-project.

GSD configuration for /full-development:
- Research before planning: YES (research synthesizer runs first)
- Verify plan before execution: YES (user approves before any code runs)
- Verify work after each phase: YES
- Execution model: sequential (not parallel — parallel risks incomplete
  phases if credits run out mid-build)
- Planning depth: standard (5–8 phases, 3–5 tasks each)

GSD research synthesizer runs parallel sub-agents to:
- Investigate the domain being changed
- Identify gaps in the current spec or plan
- Surface security, performance, or integration risks
- Confirm third-party API availability and constraints

GSD produces the phase plan in `.gsd/planning/`.

**Phase pre-validation (mandatory before presenting plan):**
Read the pre-validation rule in context-guardian.md.
Estimate token consumption per phase. Split any phase over 80k tokens.
Announce any splits made.

Present the revised plan for user approval:
```
Phase plan ready ([N] phases after pre-validation splits):
  Phase 1: [name] — [N] tasks — estimated [Xk] tokens
  Phase 2: [name] — [N] tasks — estimated [Xk] tokens
  ...
  Total across sessions: ~[X]k tokens (midpoint)

Research findings: [brief summary of anything discovered by synthesizer]

Approve this plan? YES to proceed to Ralph gate / REVISE to adjust
```

Wait for explicit YES or REVISE. Do not proceed without approval.

---

## Step 3 — Ralph Loop gate (always shown)

Read ~/.claude/skills/shared/ralph-loop-gate.md.

Always present the gate for /full-development.

Include the brownfield risk warning (see ralph-loop-gate.md).
Recommend manual mode for brownfield overhauls unless the user has
reviewed every phase plan line by line.

Wait for explicit YES or NO.

---

## Step 4 — Superpowers TDD execution

For every task in every phase, without exception:

1. **RED**: write the failing test. Confirm it fails before writing code.
2. **GREEN**: write the minimal implementation. Make the test pass.
3. **REFACTOR**: improve the code without changing behaviour.
4. Commit after each task. Commit message = root cause or feature name,
   not a vague description.

After all tasks in a phase complete:
- Superpowers /code-review runs (spec compliance + code quality)
- Fix all critical and high issues before advancing to the next phase
- Present phase completion summary before loading the next phase

If autonomous mode (Ralph Loop YES):
Each phase runs in a fresh headless session via `claude -p`.
Context guardian 50% hard stop applies within each headless session.
Phase summaries accumulate in `.gsd/planning/`.

If manual mode (Ralph Loop NO):
Present each phase plan before executing it.
Wait for approval. Execute. Wait for approval of next phase.

---

## Step 5 — Full delivery gate

Read ~/.claude/skills/shared/delivery-gate.md — Variant B (Full).

Run in sequence after all phases complete:
1. Superpowers /code-review
2. G Stack /review (security + completeness + architecture)

Add G Stack /qa if any UI changes were made.

Add G Stack /land-and-deploy if the build is being deployed to production.

Do not create a PR until the gate returns PASS with zero critical/high issues.

---

## Token budget

Expected: 200k+ tokens across all sessions.
Each phase session targets under 60k tokens (50% of 200k window minus startup).
Model: Opus for grill-with-docs and GSD research synthesizer.
Sonnet for all execution, review, and delivery.
Context guardian 50% hard stop applies in every session, including headless.
