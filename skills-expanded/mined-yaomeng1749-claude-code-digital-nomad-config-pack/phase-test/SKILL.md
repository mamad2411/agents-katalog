---
name: phase-test
description: Phase 4 of the software delivery workflow: run unit, integration, E2E, regression, coverage, and lightweight security checks against the current change set.
origin: ECC automation-pack
---

# Phase Test

Use this skill when the user asks for `/phase-test`, test phase, regression testing, coverage checks, or validation after implementation.

## Purpose

Prove that the implementation works and did not break nearby behavior.

## Workflow

1. Identify the project’s test commands from package files, CI config, docs, or existing scripts.
2. Run the smallest relevant tests first, then broader suites.
3. Prefer standard commands such as:
   - `npm test`, `pnpm test`, `bun test`
   - `pytest`
   - `go test ./...`
   - `cargo test`
   - Maven/Gradle test commands
4. Check coverage when the project already supports it, targeting the project’s configured threshold or 80% where no threshold exists.
5. Run E2E tests when the change affects user flows and E2E infrastructure exists.
6. Run lightweight security checks:
   - obvious secret leaks
   - unsafe input handling
   - auth/authorization regressions
   - injection-prone code paths
7. Summarize failures with reproduction commands.

## Output

Include:

- commands run
- pass/fail results
- coverage result when available
- security quick-scan notes
- remaining test gaps

End with `PHASE_TEST_DONE` when checks pass, or `PHASE_TEST_FAILED` with failure details.
