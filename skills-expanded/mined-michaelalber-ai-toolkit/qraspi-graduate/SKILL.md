---
name: qraspi-graduate
audience: team
description: >
  QRASPI Graduation — the terminal handoff from greenfield (QRASPI) to brownfield (QRSPI). Once
  the walking skeleton is green and V0/V1 ships, captures repo + accepted ADRs + skeleton state
  + fitness functions + stack into graduation.md and hands new feature work to QRSPI. Use for
  '/qraspi-graduate <project>', 'graduate this to QRSPI', 'V1 is done, hand off to the feature
  workflow'. Do not fire mid-workflow or on a generic 'we are done'/'ship it' — this is the END
  of QRASPI. Not for the deprecated RPI workflow.
---

# QRASPI Graduate

> "A walking skeleton is grown, not thrown away. Once it walks and carries real features, it is just... the codebase."

## Core Philosophy

QRASPI is **V0/V1 only**. Once the walking skeleton is green and the first real slices are shipped,
new features stop being greenfield -- they are additions to an existing codebase, which is QRSPI's
job. Graduation is the explicit seam: a single markdown artifact, `graduation.md`, that bootstraps the
first QRSPI feature with everything QRASPI produced -- the repo, the accepted ADRs, the layers the
skeleton exercises, the live fitness gates, and the stack declaration. Both workflows already share
`tdd-loop`, vertical slices, and the read-only `research-*` subagents, so the seam is **state capture +
documentation, not new machinery**.

**Non-Negotiable Constraints:**
1. SKELETON-GATED + TERMINAL -- never graduate without `skeleton.md` (status: complete, `ci_green:
   true`); never fire mid-workflow. V0/V1 must be shipped (the skeleton stands green AND the first
   slices are built, or the human explicitly confirms V1 is done)
2. CAPTURE, DON'T RE-DERIVE -- `graduation.md` indexes what already exists (the repo, `docs/adr/`,
   `skeleton.md`, the fitness gates, the stack); it adds no new decisions and re-opens nothing
3. NO NEW MACHINERY -- the seam is documentation only. Write one artifact, hand off, stop
4. EXPLICIT HANDOFF -- `graduation.md` ends with the QRSPI bootstrap instruction (run /qrspi-questions
   in this repo); after it, QRASPI is complete for this system
5. CONTEXT BUDGET: keep utilization under 40%. At 60%, write `graduation.md` with progress and tell
   the user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Locate the project folder thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
    [ ] Read skeleton.md (status: complete, ci_green: true). If absent / not green -> STOP; route to /qraspi-skeleton
    [ ] Confirm V0/V1 is shipped: implementation-log-{slice}.md present for the built slices, or the
        human explicitly confirms V1 is done. If nothing is built yet -> STOP; this is mid-workflow, not graduation
    [ ] Read the accepted docs/adr/, the live fitness gates, and the stack declaration

CAPTURE  (index what exists -- no new decisions)
    Assemble graduation.md (references/graduation-template.md) from:
      1. Target repo pointer + docs/adr/ (the accepted ADRs QRSPI will read)
      2. Skeleton state -- the layers the walking skeleton exercises + current CI status
      3. The landed fitness functions + where each gates
      4. The stack declaration
      5. The QRSPI handoff instruction

WRITE
    thoughts/shared/qraspi/YYYY-MM-DD-{slug}/graduation.md (status: complete)

REPORT
    graduation.md path · what was captured · "V0/V1 is shipped. New features now use QRSPI --
    run /qrspi-questions in this repo." QRASPI is complete for this system.
```

**Exit criteria:** `graduation.md` written capturing the repo + accepted ADRs + skeleton state +
landed fitness functions + stack; it ends with the QRSPI handoff instruction; the user is told QRASPI
is complete for this system and to run `/qrspi-questions` for the next feature.

## State Block

```
<qraspi-graduate-state>
phase: PRE-FLIGHT | CAPTURE | WRITE | REPORT | COMPLETE
project_folder: thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
skeleton_present: true | false        # MUST be true to proceed
skeleton_ci_green: true | false       # MUST be true to proceed
v1_shipped: true | false              # MUST be true -- the terminal guard, not mid-workflow
adrs_captured: [count]
fitness_gates_captured: [count]
stack_declared: [stack | unknown]
handoff_written: true | false         # the /qrspi-questions instruction is in graduation.md
context_budget: under-40 | approaching-60 | checkpoint-now
status: in_progress | complete
</qraspi-graduate-state>
```

## Output Template

See `references/graduation-template.md` for the `graduation.md` structure -- the repo + ADR pointer,
the skeleton state, the landed fitness functions, the stack declaration, and the QRSPI handoff block.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qraspi-skeleton` | Source of the skeleton state + the live fitness gates `graduation.md` captures. |
| `qraspi-implement` | Its `implementation-log-{slice}.md` files are the evidence that V0/V1 is shipped (the terminal precondition). |
| `qraspi-architecture` | The accepted ADRs `graduation.md` points QRSPI at -- QRSPI reads them to understand the locked decisions. |
| `qrspi-questions` | The QRSPI entry point this phase hands off to -- new features run `/qrspi-questions` in the same repo. |
| `research-file-locator` / `research-code-analyzer` / `research-pattern-finder` | The read-only subagents QRSPI's Research uses (inherited-repo mode) to map the now-existing codebase QRASPI produced. |
