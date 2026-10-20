---
name: itsol-tdd-workflow
description: "Use RED-GREEN-REFACTOR only when the user explicitly requests test-first development."
---

# ITSOL TDD Workflow

This is an optional method for an explicitly requested test-first task. Do not select it merely because code behavior changes, a test framework exists, or legacy `.itsol.md` metadata says TDD is supported. Ordinary work uses the router's proportionate verification contract without RED/GREEN or an exception gate.

## Requested test-first loop

1. State the observable behavior or regression.
2. Inspect supported tests and relevant `.itsol.md` verification constraints.
3. Choose one meaningful behavior-level test and run it: **RED** must fail for the behavior, not setup.
4. Implement the coherent change for **GREEN**; rerun the affected check and broaden only for concrete risk or required policy.
5. Refactor only after GREEN and rerun the focused check after meaningful cleanup.

A useful test protects externally observable behavior or a real contract and remains valid after a refactor. Reuse existing coverage where it proves the requested behavior. Avoid tests per helper/function, mock-call counts, private structure, trivial assertions, and duplicate fixtures.

## Practical limits

If no maintained test harness can prove the behavior safely, report that limitation and propose a proportionate check. Introduce test infrastructure only when it is explicitly requested or included in agreed scope. Missing TDD support does not block unrelated authorized work.

## Handoff

For the explicitly requested TDD task, report the behavior protected, RED/GREEN commands and observed results, relevant verification, and limitations. Load `itsol-execution-policy` when resource, stop, delegation, or completion state matters; preserve `partial`, `blocked`, and `failed` instead of inferring completion from termination or `maxTurns`.
