---
name: qraspi-implement
audience: team
description: >
  QRASPI Implement phase — grows the green walking skeleton ONE approved slice at a time with
  strict Red-Green-Refactor per phase, keeping fitness gates green, and writes a per-slice proof
  log. Use for '/qraspi-implement <project>', 'implement the slice on the skeleton', 'build the
  approved plan-{slice} with RGR'. Requires plan-{slice}.md status: approved and a green
  skeleton. Not for a feature in an EXISTING codebase (qrspi-implement), the deprecated RPI
  workflow, or a bare TDD cycle with no plan (tdd-loop).
---

# QRASPI Implement

> "Amateurs practice until they get it right; professionals until they can't get it wrong."

## Core Philosophy

The Implement phase grows the walking skeleton **one approved slice at a time**. Architecture locked
the decisions, Plan made the slice mechanical -- you execute `plan-{slice}.md` without re-opening
either. Each phase inside the slice plan runs a full **Red-Green-Refactor** loop, with RED and GREEN
command output captured to the slice's log. The skeleton's **fitness gates are live**, so GREEN means
tests pass *and* gates stay green. One slice is ideally one fresh session -- the per-slice log is the
resumption point. You stop the instant the plan does not cover something.

**Non-Negotiable Constraints:**
1. APPROVED-GATED -- never start without `plan-{slice}.md` status: approved; never implement from memory
2. SKELETON GREEN FIRST -- pre-flight requires `skeleton.md` `ci_green: true` AND a green baseline run
   (tests + fitness gates); a red baseline is a STOP, not yours to fix
3. ONE SLICE, PHASES IN ORDER -- execute the phases inside `plan-{slice}.md` in order; never reorder,
   parallelize, or skip; other backlog slices are out of scope for this run
4. RGR PER PHASE, GATES STAY GREEN -- RED (test fails) -> GREEN (minimal code, build+test+fitness
   gates pass) -> REFACTOR (stays green); a tripped gate is fixed, never disabled
5. RECORD THE PROOF -- write RED and GREEN command output to `implementation-log-{slice}.md`
6. INVENTION = STOP -- anything not in the plan stops the slice (re-run /qraspi-plan); a design change
   routes to /qraspi-architecture. Never improvise.
7. CONTEXT BUDGET: keep utilization under 40%. At 60% (or end of the slice), checkpoint to the slice
   log and tell the user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Locate the project folder thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
    [ ] Read skeleton.md: status: complete AND ci_green: true. If not green -> STOP; route to /qraspi-skeleton
    [ ] Read plan-{slice}.md for the target slice. If absent -> STOP; route the user to /qraspi-plan
    [ ] Confirm plan-{slice}.md status: approved (else STOP, ask the human) and run the baseline suite
        (tests + fitness gates). If red -> STOP; report; do not fix it
    [ ] Read the ENTIRE plan-{slice}.md; identify the next unfinished phase from implementation-log-{slice}.md

PHASE LOOP  (one phase = one vertical increment inside the slice; inner loop delegated to tdd-loop)
    1. RED   — write the phase's failing test; RUN it; it MUST FAIL. If it passes, fix the test.
    2. GREEN — write the minimal production code; RUN build + tests + fitness gates; ALL MUST PASS.
    3. REFACTOR — clean up; RUN again; it MUST stay GREEN (tests AND gates).
    4. RECORD — append to implementation-log-{slice}.md: RED output, GREEN output, gate result, files changed.
    5. CHECKPOINT — suggest a commit; if context > 40% or the slice is done, hand off a fresh session.

REPORT
    Phases complete / total · fitness gates green · next backlog slice (/qraspi-plan) or
    "all backlog slices built -> /qraspi-graduate".
```

**Exit criteria:** every phase in `plan-{slice}.md` executed with RED + GREEN proof logged;
build/tests AND fitness gates GREEN; the user knows the next slice or that the system can graduate.

## State Block

```
<qraspi-implement-state>
phase: PRE-FLIGHT | RED | GREEN | REFACTOR | RECORD | CHECKPOINT | COMPLETE
project_folder: thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
skeleton_ci_green: true | false      # MUST be true to proceed
plan_present: true | false           # plan-{slice}.md -- MUST be true to proceed
plan_approved: true | false          # MUST be true to proceed
baseline_green: true | false         # tests + fitness gates -- MUST be true before any change
slice_name: [the slice being built]
current_phase: [NN]
phases_total: [count]
phases_complete: [count]
fitness_gates_green: true | false    # MUST stay true -- it is part of GREEN
last_verification: red | green | pending   # RED step expects red; GREEN/REFACTOR expect green
context_budget: under-40 | approaching-60 | checkpoint-now
</qraspi-implement-state>
```

## Output Template

See `references/implementation-log-template.md` for the per-slice `implementation-log-{slice}.md`
structure -- the per-phase RED/GREEN proof, gate result, files changed, and resume note.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qraspi-plan` | Prior phase. Its approved `plan-{slice}.md` is the contract this phase executes. |
| `qraspi-skeleton` | Supplies the green skeleton this phase grows on and the live fitness gates GREEN must keep passing. |
| `tdd-loop` | The inner loop each phase runs -- the test-first mechanics this skill enforces per phase. |
| `qraspi-graduate` | Terminal next step once every backlog slice is built -- hands the repo to QRSPI. |
| `dotnet-vertical-slice` / `python-feature-slice` / `rust-feature-slice` | Stack scaffolders for the slice's phases. |
| `qrspi-implement` | Brownfield sibling: same per-slice RGR, on an existing codebase's `plan.md`. |
