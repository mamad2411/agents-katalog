---
name: qraspi-plan
audience: team
description: >
  QRASPI Plan phase — converts the next slice from the skeleton backlog into a mechanically
  executable, vertically-sliced plan-{slice}.md with exact file paths and per-phase
  verification, grown on the green walking skeleton. Use for '/qraspi-plan <project>', 'plan the
  first slice of new X', 'plan the next increment on the skeleton'. Consumes skeleton.md and
  REFUSES horizontal-layer plans. Not for a feature in an EXISTING codebase (qrspi-plan) or the
  deprecated RPI workflow.
---

# QRASPI Plan

> "A plan precise enough to execute mechanically is the goal." -- adapted from Eisenhower

## Core Philosophy

Greenfield grows **one vertical slice at a time on top of the green walking skeleton**. Skeleton
already stood the architecture up, landed the fitness gates, and enumerated a slice backlog; Plan
takes the **next unbuilt backlog slice** and makes it mechanically executable -- exact file paths, a
test-first step per phase, an automated verification command -- without re-opening the architecture.
Its one hard gate is **vertical, not horizontal**: a slice plan organized by technical layer (all
models, then all services, then all UI) is rejected before it is written.

**Non-Negotiable Constraints:**
1. SKELETON-GATED -- never plan without `skeleton.md` (status: complete, `ci_green: true`) on disk;
   the slice comes from the skeleton's backlog, never from memory
2. ONE BACKLOG SLICE -- plan the next unbuilt slice from `skeleton.md`'s backlog (default), producing
   `plan-{slice}.md`; never re-plan a built slice or invent scope the backlog does not name
3. VERTICAL OR REFUSE -- if the slice's phases organize by horizontal layer, STOP and re-slice first
4. MECHANICAL, NO SOURCE -- every change names an exact file path; descriptions and illustrative
   snippets only, never full implementations. "The service layer" is not a path.
5. ARCHITECTURE-RESPECTING -- honor the accepted ADRs and fitness gates; a plan whose verification
   would fail a gate is invalid. Do NOT re-open the ADRs -- that is /qraspi-architecture
6. CONTEXT BUDGET: keep utilization under 40%. At 60%, write `plan-{slice}.md` with progress and
   tell the user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Locate the project folder thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
    [ ] Read skeleton.md. If absent -> STOP; route to /qraspi-skeleton
    [ ] Confirm status: complete AND ci_green: true -- else STOP; it must stand up green first
    [ ] Read the SLICE BACKLOG; pick the next unbuilt slice (default) or the one the user named
    [ ] Skim the accepted docs/adr/ + the fitness gates this slice's verification must keep green

RE-SLICE GATE  (the vertical-not-horizontal refusal)
    Inspect the intended phases. If any phase completes a whole layer (all models, then all
    services, then all UI), STOP and re-slice so each phase is an end-to-end increment.

WRITE  (only after the gate passes)
    For the chosen backlog slice: exact file paths · change descriptions · a RED test step before
    the code step · a verification command (tests AND fitness gates) · a rollback line ·
    "What we're NOT doing" (scope boundaries). Write plan-{slice}.md, status: ready-for-review.

REPORT
    Artifact path · slice planned · phase list · backlog remaining ·
    "Review/approve, then start a NEW session and run /qraspi-implement"
```

**Exit criteria:** `plan-{slice}.md` holds vertically-sliced phases for ONE backlog slice, each with
exact paths, a test-first step, a verification command that keeps the fitness gates green, and a
rollback; a "What we're NOT doing" list is present; `status: ready-for-review`.

## State Block

```
<qraspi-plan-state>
phase: PRE-FLIGHT | RE-SLICE-GATE | WRITE | REPORT | COMPLETE
project_folder: thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
skeleton_ci_green: true | false       # MUST be true to proceed
slice_name: [the backlog slice being planned]
slice_from_backlog: true | false      # MUST be true -- no invented scope
phases_planned: [count]
vertical_check: pass | re-slice-needed   # MUST be pass before WRITE
fitness_gates_respected: true | false    # verification keeps the skeleton's gates green
rollback_documented: true | false
backlog_remaining: [count]
context_budget: under-40 | approaching-60 | checkpoint-now
status: draft | ready-for-review | approved
</qraspi-plan-state>
```

## Output Template

See `references/plan-slice-template.md` for the full `plan-{slice}.md` structure, per-phase shape
(paths, RED/GREEN steps, verification, rollback), and the horizontal-vs-vertical worked example.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qraspi-skeleton` | Prior phase. Its `skeleton.md` backlog is the source of the slice; its fitness gates constrain the plan's verification. |
| `qraspi-implement` | Next phase. Consumes the approved `plan-{slice}.md`; refuses to run without `status: approved`. |
| `qraspi-architecture` | The accepted ADRs the plan must respect, not re-open -- a design change routes back there. |
| `tdd-loop` | The inner loop Implement runs per phase; Plan's test-first steps map onto RED-GREEN-REFACTOR. |
| `dotnet-vertical-slice` / `python-feature-slice` / `rust-feature-slice` | Stack scaffolders for the slice. |
| `qrspi-plan` | Brownfield sibling: same horizontal-refusal gate, on an existing codebase's single `plan.md`. |
