---
name: qrspi-implement
audience: team
description: >
  QRSPI Implement phase -- executes an approved plan.md slice-by-slice with strict Red-Green-Refactor
  per slice and a fresh-session checkpoint after each. Use for "/qrspi-implement <feature>", "execute
  the qrspi plan", "build the approved plan slice by slice". Not for a bare TDD cycle with no plan
  (use tdd-loop); this phase requires plan.md status: approved and writes per-slice logs.
---

# QRSPI Implement

> "Amateurs practice until they get it right. Professionals practice until they can't get it wrong."

## Core Philosophy

The Implement phase executes an already-approved plan mechanically -- every design decision was
settled by Spec and Plan. Each plan phase is one **vertical slice**, and each slice runs the full
**Red-Green-Refactor** loop end-to-end before the next begins. The discipline is test-first and
per-slice: a slice is not done until its RED proof and GREEN proof are recorded on disk. One slice is
ideally one fresh session -- the per-slice log is the resumption point, so context never has to span
the whole feature.

**Non-Negotiable Constraints:**
1. APPROVED-GATED -- never start without `plan.md` status: approved; never implement from memory
2. BASELINE GREEN FIRST -- run the test suite before any change; a red baseline is a STOP, not yours to fix
3. ONE SLICE AT A TIME -- execute plan phases in order; never reorder, parallelize, or skip
4. TEST FIRST OR STOP -- production code written before a failing test is a STOP condition
5. RGR PER SLICE -- RED (test fails) -> GREEN (minimal code, build+test pass) -> REFACTOR (stays green)
6. RECORD THE PROOF -- write RED and GREEN command output to `implementation/slice-NN-{name}.md`
7. INVENTION = STOP -- anything not in the plan stops the slice; re-run /qrspi-plan, do not improvise
8. CONTEXT BUDGET: keep utilization under 40%. At 60% (or end of a slice), checkpoint to the slice log
   and tell the user to start a fresh session for the next slice.

## Workflow

```
PRE-FLIGHT
    [ ] Locate the feature folder thoughts/shared/qrspi/YYYY-MM-DD-{slug}/
    [ ] Read plan.md. If absent -> STOP; route the user to /qrspi-plan
    [ ] Confirm plan.md status: approved. If only ready-for-review -> STOP; ask the human to approve
    [ ] Run the baseline test suite. If red -> STOP; report; do not fix the baseline
    [ ] Read the ENTIRE plan; identify the next unfinished slice from implementation/

SLICE LOOP  (one slice = one plan phase, ideally one fresh session)
    1. RED   — write the failing test from the phase; RUN it; it MUST FAIL.
               If it passes, the test is wrong -> fix the test, not the code.
    2. GREEN — write the minimal production code; RUN build + tests; they MUST PASS.
    3. REFACTOR — clean up; RUN again; it MUST stay GREEN.
    4. RECORD — write implementation/slice-NN-{name}.md: RED output, GREEN output, files changed.
    5. CHECKPOINT — suggest one commit for the slice; if context > 40% or the slice is done,
                    tell the user to start a fresh session for the next slice.

REPORT
    Slices complete / total · last verification result · next slice (or "feature complete").
```

**Exit criteria:** each executed slice has a `slice-NN-{name}.md` log holding its RED proof and GREEN
proof; the build/tests are GREEN; a per-slice commit was suggested; the user knows the next slice or
that the feature is complete.

## State Block

```
<qrspi-implement-state>
phase: PRE-FLIGHT | RED | GREEN | REFACTOR | RECORD | CHECKPOINT | COMPLETE
feature_folder: thoughts/shared/qrspi/YYYY-MM-DD-{slug}/
plan_present: true | false          # MUST be true to proceed
plan_approved: true | false         # MUST be true to proceed
baseline_green: true | false        # MUST be true before any change
current_slice: [NN]
slices_total: [count]
slices_complete: [count]
last_verification: red | green | pending   # RED step expects red; GREEN/REFACTOR expect green
context_budget: under-40 | approaching-60 | checkpoint-now
</qrspi-implement-state>
```

## Output Template

See `references/slice-log-template.md` for the per-slice `implementation/slice-NN-{name}.md`
structure -- the RED proof, GREEN proof, files-changed list, and the resume note.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qrspi-plan` | Prior phase. Its approved `plan.md` is the contract this phase executes; refuses to run without `status: approved`. |
| `tdd-loop` | The inner loop. Each slice IS a RED-GREEN-REFACTOR cycle; load `tdd-loop` for the test-first mechanics this skill enforces per slice. |
| `dotnet-vertical-slice` / `python-feature-slice` / `rust-feature-slice` | Stack scaffolders for the slice each phase builds. |
