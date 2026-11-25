---
name: nestjs-11-quality-gates
description: Runs and interprets safe NestJS 11 quality checks, including lint, tests, build, type checking, static DTO/boundary heuristics, service-test reminders, and conservative command safety. Use when validating changes, debugging failing tests, or preparing work for review.
license: MIT
compatibility: "For NestJS 11.x repositories with Node.js package scripts. Scripts require bash, node, and optionally git."
---

# NestJS 11 Quality Gates

This skill helps agents verify NestJS 11 changes safely and debug failures without hiding real problems.

## When to Use This Skill

Use this skill when:

- The user asks to run or fix tests.
- A NestJS 11 change is ready for verification.
- Lint, type check, build, or test commands fail.
- A command might mutate dependencies, delete data, reset migrations, or install incompatible `@nestjs/*` versions.
- The agent needs a lightweight local quality checklist.
- Controller DTO validation, module boundaries, or service test coverage need a conservative static review.

## Scripts

Scripts are stored under this skill:

- `scripts/nestjs-11-command-safety.sh`
- `scripts/nestjs-11-detect-project-package-manager.sh`
- `scripts/nestjs-11-local-quality-check.sh`
- `scripts/nestjs-11-dto-validation-check.sh`
- `scripts/nestjs-11-boundary-import-check.sh`
- `scripts/nestjs-11-service-test-suggestion.sh`

Before running any script manually, run it with `--help`.

## Workflow References

Use these workflows:

- `workflows/local-quality-workflow.md` for normal verification.
- `workflows/failing-test-debug-workflow.md` for failing test repair.

## Resource References

Read when relevant:

- `resources/quality-gate-matrix.md`
- `resources/common-failures.md`

## Example References

- `examples/testing-module-example.md`

## Quality Principles

- Run the smallest relevant check first.
- Prefer repository-provided package scripts.
- Do not install packages, update lockfiles, reset databases, or rewrite snapshots without explicit user approval.
- Do not mark work complete if required checks were skipped without explanation.
- Never weaken tests merely to make the suite pass.
- Treat hook findings as prompts for review, not as proof of a bug.
- If SWC is used, ensure type checking is still covered by a script such as `tsc --noEmit`, `nest build`, or a repository-specific check.
