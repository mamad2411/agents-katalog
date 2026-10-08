---
name: "full-test-suite"
description: "Run the project-ops skill bundle end to end: health, bug, security, API contract, docs, and issue reconciliation, then plan and apply verified fixes one at a time until no confirmed-open findings remain. Use when a user asks for a full repository audit, project ops sweep, or bundled scan-fix-verify loop across the skill suite."
---

# Full Test Suite

Run the project-ops skill bundle as a meta-skill backed by a deterministic runner. The default mode is audit-then-fix.

## Script-Backed Entry Point

Use `scripts/full_test_suite_runner.py` to initialize the run, track skill execution, persist `full-test-suite-manifest.json`, refresh the fix queue, suggest impacted reruns, run deterministic GitHub issue sync, and finalize `full-test-suite-report.md`. When you want the suite to actually drive itself through those next actions, use `scripts/full_test_suite_executor.py`.

At the start of a bundle run:

1. Run `python3 scripts/full_test_suite_runner.py init --repo-root . --findings-path project-audit-findings.md --report-path full-test-suite-report.md --manifest-path full-test-suite-manifest.json --scope "<scope>" --mode <mode> --profile <profile>`.
2. Use `../_shared-project-ops/scripts/project_ops_state.py` to upsert or merge findings in `project-audit-findings.md`.
3. Drive the bundle from `python3 scripts/full_test_suite_runner.py next-action --manifest-path full-test-suite-manifest.json`.
4. After each completed fix, record it with `python3 scripts/full_test_suite_runner.py record-fix --manifest-path full-test-suite-manifest.json --finding-id <id> --surfaces "<paths>" --types "<types>"`.
5. When `next-action` returns `sync-issues`, run `python3 scripts/full_test_suite_runner.py sync-issues --manifest-path full-test-suite-manifest.json`.
6. Finalize only after `next-action` returns `finalize`, using `python3 scripts/full_test_suite_runner.py finalize --repo-root . --findings-path project-audit-findings.md --report-path full-test-suite-report.md --manifest-path full-test-suite-manifest.json`.

## Supported Modes

- default: full core audit, issue sync, fix queue, one-by-one fix and verify loop
- `mode=scan-only`: no code fixes; produce findings and issue updates only
- `mode=rerun-impacted`: rerun affected skills after recent fixes
- `mode=resume`: continue from existing `project-audit-findings.md` and issue state

## Core Sequence

1. Initialize run context: repo root, branch, dirty worktree, `gh` availability, and constraints.
2. Run `$project-health-check`.
3. Run `$bug-hunter`.
4. Run `$security-audit-lite`.
5. Run `$api-contract-auditor`.
6. Run `$docs-sync`.
7. Run `$issue-operator`.
8. Consolidate findings and dedupe root causes.
9. Build a fix queue from confirmed findings only.
10. Fix and verify one confirmed finding at a time.
11. Rerun only impacted skills.
12. Require a clean post-fix full scan with no new actionable findings.
13. Finalize `full-test-suite-report.md` and `full-test-suite-manifest.json`.

## Decision Rules

- `project-audit-findings.md` is the shared local source of truth.
- Only `confirmed-open` findings enter the fix queue.
- Group only tightly related fixes.
- Close GitHub issues only after verification evidence is recorded locally.
- Stop when no `confirmed-open` or `in-progress` findings remain.
- Keep `blocked` and `needs-context` items clearly separated in the final report.
- Preserve unrelated dirty worktree changes; do not revert or restage files outside the current fix.
- Ask before destructive repository or GitHub administration operations unless the user explicitly requested that class of action.
- Prefer focused reruns after each fix rather than broad churn that obscures causality.

## Profiles

- `core`: phase-1 skills only
- `pre-release`: add `$release-readiness`, `$test-gap-finder`, `$dependency-risk-review`, and `$refactor-safety-check`
- `deep-audit`: add `$onboarding-doc-builder`, `$observability-gap-review`, `$config-drift-auditor`, `$data-model-migration-review`, and `$frontend-regression-review`

If a profile references a skill that is unavailable or out of scope, record the skip in `full-test-suite-report.md`.

## Outputs

- `project-audit-findings.md`
- `full-test-suite-report.md`
- `full-test-suite-manifest.json`

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- State CLI: `../_shared-project-ops/references/state-cli.md`
- Execution report format: `../_shared-project-ops/references/execution-report-format.md`
- Dedupe rules: `../_shared-project-ops/references/dedupe-rules.md`
- Rerun policy: `../_shared-project-ops/references/rerun-policy.md`
- Verification template: `../_shared-project-ops/references/verification-template.md`
- Runner usage: `references/runner-usage.md`
- Manifest loop: `references/manifest-loop.md`
- Executor: `references/executor.md`
