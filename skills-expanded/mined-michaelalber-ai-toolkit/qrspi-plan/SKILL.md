---
name: qrspi-plan
audience: team
description: >
  QRSPI Plan phase -- converts an approved spec.md into a mechanically executable, vertically
  sliced plan.md with exact file paths and per-phase verification. Use for "/qrspi-plan <feature>",
  "qrspi plan X", "turn the spec into an implementation plan". Not for planning without a spec; this
  phase consumes spec.md and REFUSES horizontal-layer plans.
---

# QRSPI Plan

> "A plan precise enough to execute mechanically is the goal. If the implementer has to invent anything, the plan failed."
> -- Adapted from Dwight D. Eisenhower

## Core Philosophy

The Plan phase turns the approved spec into an implementation contract the Implement phase can
execute WITHOUT judgment, invention, or discovery. The spec already settled the design and the
vertical slices; Plan makes each slice mechanical -- exact file paths, exact changes, a test-first
step, and an automated verification command. Its one hard gate is **vertical, not horizontal**: a
plan organized by technical layer (all models, then all services, then all UI) is rejected before
it is written. Each phase must deliver an end-to-end testable increment, inherited from the spec's
slices.

**Non-Negotiable Constraints:**
1. SPEC-GATED -- never plan without an approved `spec.md` on disk; never plan from memory
2. VERTICAL OR REFUSE -- if phases organize by horizontal layer, STOP and re-slice before writing
3. MECHANICAL EXECUTION -- every change names an exact file path; "the service layer" is not a path
4. TESTS FIRST -- any phase adding behavior opens with a failing-test step (RED) before the code step
5. EVERY PHASE VERIFIABLE -- each phase carries an automated command (build / test / lint) and a rollback
6. NO SOURCE CODE -- change descriptions and illustrative snippets only, never full implementations
7. CONTEXT BUDGET: keep utilization under 40%. At 60%, write `plan.md` with progress and tell the
   user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Locate the feature folder thoughts/shared/qrspi/YYYY-MM-DD-{slug}/
    [ ] Read spec.md. If absent -> STOP; route the user to /qrspi-spec
    [ ] Confirm spec.md status: approved AND design_approved: true.
        If only ready-for-review -> STOP; ask the human to approve the spec design first
    [ ] Carry the spec's Structure Outline slices forward as the phase skeleton

RE-SLICE GATE  (the vertical-not-horizontal refusal)
    Inspect the intended phases. If any phase completes a whole layer (all models, then all
    services, then all UI), STOP and re-slice so each phase is an end-to-end increment.
    Do NOT proceed to WRITE until every phase is a vertical slice.

WRITE  (only after the gate passes)
    For each slice/phase: exact file paths · REMOVE/ADD change descriptions · a RED test step
    before the code step · an automated verification command · a rollback line.
    Add "What we're NOT doing" (scope boundaries) and a rollback plan.
    Write plan.md, status: ready-for-review.

REPORT
    Artifact path · phase list (one line each) · "Review/approve, then start a NEW session and run /qrspi-implement"
```

**Exit criteria:** `plan.md` holds vertically sliced phases, each with exact paths, a test-first
step, an automated verification command, and a rollback; a "What we're NOT doing" list is present;
`status: ready-for-review`; user told to review/approve before `/qrspi-implement`.

## State Block

```
<qrspi-plan-state>
phase: PRE-FLIGHT | RE-SLICE-GATE | WRITE | REPORT | COMPLETE
feature_folder: thoughts/shared/qrspi/YYYY-MM-DD-{slug}/
spec_present: true | false          # MUST be true to proceed
spec_approved: true | false         # MUST be true to proceed
phases_planned: [count]
vertical_check: pass | re-slice-needed   # MUST be pass before WRITE
tests_first_phases: [count]
rollback_documented: true | false
context_budget: under-40 | approaching-60 | checkpoint-now
status: draft | ready-for-review | approved
</qrspi-plan-state>
```

## Output Template

See `references/plan-template.md` for the full `plan.md` structure, frontmatter, per-phase shape
(exact paths, RED/GREEN test steps, verification commands, rollback), and the horizontal-vs-vertical
worked example.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qrspi-spec` | Prior phase. Its approved `spec.md` (vertical slices + signatures) is the contract this phase makes mechanical. |
| `qrspi-implement` | Next phase. Consumes the approved `plan.md`; refuses to execute without `status: approved`. |
| `tdd-loop` | The inner loop the Implement phase runs per phase; Plan's test-first steps map onto RED-GREEN-REFACTOR. |
| `dotnet-vertical-slice` / `python-feature-slice` / `rust-feature-slice` | Stack scaffolders for the vertical slices each phase implements. |
