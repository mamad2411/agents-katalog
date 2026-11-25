---
name: qraspi-skeleton
audience: team
description: >
  QRASPI Skeleton phase — stands up a RUNNABLE walking skeleton for a NEW system: scaffolds the
  repo from accepted ADRs, walks one vertical slice end-to-end through every layer, lands the
  specified fitness functions as CI gates, and proves it with a real CI run (exit 0). Use for
  '/qraspi-skeleton <project>', 'scaffold the walking skeleton for X', 'stand up V0 of X with
  CI'. Exit gate is CI green, not a claim. Not for a single feature slice in an existing repo
  (*-feature-slice scaffolders), QRSPI (existing codebase), or the deprecated RPI workflow.
---

# QRASPI Skeleton

> "A walking skeleton is a tiny implementation of the system that performs a small end-to-end
> function. It need not use the final architecture, but it should link the main components."
> -- Adapted from Alistair Cockburn

## Core Philosophy

The Skeleton phase makes the architecture **executable**. A walking skeleton is a tiny end-to-end
implementation that exercises every architectural layer and carries the build/test/deploy harness --
runnable from day one, grown rather than thrown away (this is what distinguishes it from a spike).
This phase consumes the accepted ADRs + `architecture.md`, selects the matching archetype recipe,
scaffolds a runnable repo around the **one** vertical slice that walks end-to-end, lands the specified
fitness functions as CI gates, and proves it with a real command: CI green, or the phase is not done.
The failure this prevents is the **aspirational skeleton** -- a scaffold that "should run" but was
never executed. `ci_green` is a captured command result, never a claim. This is why Skeleton runs on
the builder agent (edit access), on the far side of the alignment phases' edit boundary.

**Non-Negotiable Constraints:**
1. ARCHITECTURE-GATED -- never start without `architecture.md` (status: complete) + the accepted
   `docs/adr/NNNN-*.md` on disk; the stack comes from the ADRs, never invented
2. EXECUTABLE, NOT ASPIRATIONAL -- the exit gate is a real CI/test run with exit 0; `ci_green` is a
   captured command result; you CANNOT report COMPLETE with `ci_green: false`
3. ONE WALKING SLICE -- scaffold exactly one vertical slice end-to-end through every layer (delegate
   to a `*-feature-slice`/`*-scaffold` skill); breadth is later slices, not now
4. FITNESS FUNCTIONS ARE GATES -- every fitness function `architecture.md` specified is wired into CI
   as merge-blocking (delegate to `fitness-functions`); their passing is PART OF CI green
5. RECIPE, NOT RIGID REPO -- archetype recipes are instructions you adapt to the ADRs, never
   copy-paste templates; over-constraint re-introduces the magic-words trap QRASPI exists to avoid
6. CONTEXT BUDGET: keep utilization under 40%. At 60%, write `skeleton.md` with progress and tell the
   user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Locate the project folder thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
    [ ] Read architecture.md (status: complete) + the accepted docs/adr/NNNN-*.md.
        If absent -> STOP; route the user to /qraspi-architecture
    [ ] Read the fitness-function spec table from architecture.md
    [ ] DETECT archetype: match the ADR stack declaration to references/archetypes/<archetype>.md by
        name; no match -> the generic "declare-stack-and-generate" recipe

SCAFFOLD  (archetype recipe (+) feature-slice scaffolder)
    Repo layer (archetype recipe): project layout, CI workflow, health check, observability hook,
      secure-by-default config -- the repo+CI scaffold the feature-slice tools do NOT supply
    Slice layer: invoke the matching *-feature-slice / *-scaffold skill for the ONE vertical slice
      that walks every layer end-to-end

GATE  (land the fitness functions)
    For each fitness function specified in architecture.md: invoke fitness-functions to author it and
    wire it into CI as a merge-blocking gate, traced to its ADR id.

VERIFY  (the exit gate -- a real command, not a claim)
    Run the scaffolded project's CI / test suite via Bash. Require exit 0 (build + unit + lint +
    fitness gates all green). HARDWARE archetype: CI-green covers build+unit+lint+fitness; the
    device-deploy step is a DOCUMENTED MANUAL gate, not auto-run. ci_green is the captured result.
    If non-zero -> fix and re-run; never report COMPLETE with ci_green: false.

WRITE
    thoughts/shared/qraspi/YYYY-MM-DD-{slug}/skeleton.md (status: complete): what the skeleton
    instantiates, which layers it walks, CI status, the landed fitness gates, and the SLICE BACKLOG
    for /qraspi-plan.

REPORT
    skeleton.md path · archetype used · layers walked · CI status (green) · fitness gates landed ·
    slice backlog count · "Review, then start a NEW session and run /qraspi-plan"
```

**Exit criteria:** a runnable repo scaffolded from the ADR stack; the one walking slice exercises
every architectural layer; every specified fitness function wired as a merge-blocking CI gate; the
CI/test suite RAN and exited 0 (`ci_green: true`); `skeleton.md` written with the slice backlog; user
told to review before `/qraspi-plan`.

## State Block

```
<qraspi-skeleton-state>
phase: PRE-FLIGHT | SCAFFOLD | GATE | VERIFY | WRITE | REPORT | COMPLETE
project_folder: thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
architecture_present: true | false      # MUST be true to proceed
archetype: python-mcp-server | dotnet-blazor-vertical-slice | python-fastapi-service | edge-ai-device | eval-harness | generic
walking_slice: [the one end-to-end slice scaffolded]
fitness_gates_wired: [count]            # every spec'd fitness fn wired as a CI gate
ci_command: [the exact CI/test command run]
ci_green: true | false                  # MUST be true to COMPLETE -- a captured command result
hardware_manual_gate: none | [documented device-deploy step]
slice_backlog: [count]                  # slices enumerated for /qraspi-plan
context_budget: under-40 | approaching-60 | checkpoint-now
status: in_progress | complete
</qraspi-skeleton-state>
```

## Output Template

See `references/skeleton-template.md` for the `skeleton.md` structure (what the skeleton instantiates,
CI status, landed gates, slice backlog) and the recipe-not-rigid-repo principle, and
`references/archetypes/<archetype>.md` for the per-archetype repo+CI recipe: `python-mcp-server.md`,
`dotnet-blazor-vertical-slice.md`, `python-fastapi-service.md`, `edge-ai-device.md`, `eval-harness.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qraspi-architecture` | Prior phase. Its `architecture.md` + accepted ADRs declare the stack and the fitness-function spec this phase instantiates. |
| `fitness-functions` | Authors and wires each specified fitness function as a merge-blocking CI gate; their passing is part of CI green. |
| `qraspi-plan` | Next phase. Consumes the slice backlog in `skeleton.md` to plan the next vertical increment on the skeleton. |
| `dotnet-vertical-slice` / `python-feature-slice` / `rust-feature-slice` | The feature-slice scaffolders invoked for the one walking slice; the archetype recipe supplies the repo+CI layer they do not. |
| `tdd-loop` | Used from `/qraspi-implement` when growing later slices; the skeleton itself is scaffolded, not TDD'd into existence. |
| `qrspi-implement` | Brownfield sibling's execution phase. Skeleton is greenfield-only -- it stands V0 up once, then features graduate to QRSPI. |
