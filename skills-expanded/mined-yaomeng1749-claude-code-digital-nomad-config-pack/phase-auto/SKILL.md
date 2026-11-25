---
name: phase-auto
description: Orchestrate the phase workflow end to end by detecting whether the request is software delivery or solution design, then chaining the appropriate phase skills with bounded retries, status markers, and final reporting.
origin: ECC automation-pack
---

# Phase Auto

Use this skill when the user asks for `/phase-auto`, full automation, end-to-end delivery, from requirement to PR, or an unattended phased workflow.

## Purpose

Route a broad request through the correct lifecycle without losing status or verification.

## Route Selection

Use the software delivery route when the request is mainly code, bug fix, feature work, refactoring, tests, build repair, or PR delivery:

```text
phase-research -> phase-plan -> phase-implement -> phase-test -> phase-review -> phase-ship
```

Use the solution-design route when the request is mainly concept design, product/technical planning, architecture proposal, roadmap, research plan, or non-code execution:

```text
phase-design -> phase-validate -> phase-execute -> phase-verify
```

## Execution Rules

1. Announce the chosen route and why.
2. Run one phase at a time.
3. Preserve each phase output for the next phase.
4. Retry a failed phase up to 3 times only when the next fix is clear.
5. For review/validation failures, return to the previous implementation or proposal phase.
6. Stop on security risk, destructive action, unclear scope, or repeated identical failure.

## Output

Report:

- selected route
- phase status table
- total result
- artifacts created
- checks run
- blockers or skipped steps

End with `PHASE_AUTO_DONE`, `PHASE_AUTO_BLOCKED`, or `PHASE_AUTO_FAILED`.
