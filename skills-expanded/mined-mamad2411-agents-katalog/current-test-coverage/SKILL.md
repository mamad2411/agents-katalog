---
name: current-test-coverage
description: Use when a user asks for the current or latest test coverage and wants fresh coverage metrics from this session instead of previously recorded numbers.
---

# Current Test Coverage

## Specialization

Run a fresh coverage pass for the current workspace and report current coverage in grid-first format with explicit X of Y metrics.

This skill is execution-first. It gathers fresh evidence, prefers built-in dotnet tooling, and only falls back to helper scripts where built-in commands do not provide clean aggregation.

## Trigger Conditions

Use this skill when one or more are true:

- The user asks for current test coverage.
- The user asks for latest line or branch coverage.
- The user explicitly rejects stale doc-based numbers.
- The user wants a fresh coverage pass before receiving a status update.

Do not use this skill for updating historical trend docs unless the user asks for that as a separate follow-up.

## Self-Containment Requirement

Keep all execution, aggregation, and reporting steps inside this workflow.

## Built-In First Rule

Always prefer built-in workspace tools before helper scripts.

Execution order:

1. Use the skill-contained quality gate first:
   - `references/scripts/invoke-quality-gate.ps1`
2. If the standard path fails or does not satisfy the full-run request, use the built-in full-solution command:
   - `dotnet test ./Rook.sln --collect:"XPlat Code Coverage" --results-directory ./.artifacts/full-solution-coverage --nologo --verbosity minimal`
3. Use helper scripts only for repeatable artifact aggregation and formatting after the run.

## Inputs

Required:

- Workspace root.

Optional:

- Coverage scope override.
- Artifacts directory override.
- Whether to update `.docs/changes/coverage-trend.md` after reporting.

## Assets

- Standard coverage gate: `references/scripts/invoke-quality-gate.ps1`
- Fallback run helper: `references/scripts/invoke-full-solution-coverage.ps1`
- Coverage aggregation helper: `references/scripts/get-cobertura-coverage-summary.ps1`
- Script asset guide: `references/scripts/[README.md](./../../../README.md)`

## Workflow

1. Confirm the request is for current coverage, not historical coverage.
2. Run the standard repo coverage path first.
3. If the standard path fails, capture the failure reason and continue with the full-solution fallback.
4. Aggregate fresh Cobertura artifacts.
5. Report results in table-first format.
6. If project-level coverage identity is incomplete, report per-package or per-assembly coverage and explicitly state that limitation.
7. Offer a separate trend-doc update only after the fresh report is complete.

## Required Output Contract

Always return tables first.

Minimum sections:

- Summary table
- Per-project coverage table when available
- Warnings and gaps table

Every relevant table must include explicit X of Y metrics.

Always capture and report:

- Aggregate line coverage
- Aggregate branch coverage
- Test totals passed, failed, and skipped
- Run timestamp
- Run scope
- Standard path status
- Fallback path status when used

Keep non-table narrative to 3 short lines maximum.

## Reporting Rules

- Do not answer from `.docs` snapshots if a fresh run was requested.
- If the standard repo path fails before producing coverage, say so explicitly.
- If fallback coverage runs but the solution still exits non-zero, use the fresh fallback artifacts and report the failed tests in the gaps table.
- If per-test-project coverage cannot be reconstructed from artifacts, say that directly and report the closest valid fresh grouping.

## Common Mistakes

- Returning stale numbers from `coverage-trend.md` or delivery docs.
- Skipping the standard repo path.
- Treating a failed full run as “no coverage available” when Cobertura artifacts were still produced.
- Returning narrative-first output.
- Reporting percentages without X of Y values.

## Done Criteria

Coverage reporting is complete only when:

- A fresh run happened in the current session.
- The standard path was attempted first.
- Any fallback path is documented.
- Aggregate coverage is reported with X of Y values.
- Per-project or nearest-valid fresh breakdown is included.
- Missing data and failure causes are explicitly called out.

## Required Outputs

- A concrete, workspace-applicable result aligned with this skill purpose.


