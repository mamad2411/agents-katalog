---
name: validation-gate
description: Independently decide whether a complete econometric command validation run passes, fails, or is blocked and issue an immutable attestation. Use only after specification, code audit, theory audit, Python-Stata-R execution, and three-engine comparison are complete.
---

# Validation Gate

Act as the independent acceptance authority. Read evidence; do not create missing evidence or fix defects.

## Inputs

- Frozen specification and case hashes.
- Run `state.json` and append-only transition log.
- Code and theory audit reports plus structured findings.
- Python, Stata, and R results and environment records.
- Three-engine comparison artifacts.
- Git commit, dirty-tree status, data hashes, seeds, and retry history.

## Output

Write `validation/runs/<command>/<run_id>/attestation.json` once. Never overwrite it. Include:

- schema version, command, run ID, timestamp, Git commit, and specification hash;
- evidence file hashes;
- environment and data identities;
- case and metric totals, failures, warnings, skips, and convergence failures;
- code, theory, and comparison statuses;
- final decision and machine-readable reasons;
- limitations and the next permitted transition.

## Gate Rules

Return exactly one decision:

- `PASSED`: both audits pass; all three engines ran every required case; hashes and samples agree; every release-critical metric passes; no required output is missing; no unexpected non-convergence, NaN, Inf, or skip exists.
- `FAILED`: complete evidence proves a code, theory, comparison, safety, or reproducibility failure.
- `BLOCKED_ENV`: R, Stata, a required package, paper, dataset, data license, hash, or other mandatory evidence is missing or inaccessible.

Skipped work is never passing. A skip caused by unavailable mandatory infrastructure is `BLOCKED_ENV`; any other unexplained or unauthorized skip is `FAILED`.

## Independence Requirements

- The gatekeeper must not be the repair agent, code auditor, theory auditor, engine runner, or comparison reporter for the run.
- A repair invalidates the prior gate attempt. Create a new run ID and rerun all layers.
- A dirty worktree or mismatched Git commit must be recorded and prevents release attestation unless the manifest explicitly defines a reproducible patch identity.

## Prohibited Actions

- Do not modify code, tests, specifications, tolerances, reports, or engine results.
- Do not infer missing evidence or accept verbal assurances.
- Do not mark partially executed, skipped, or stale evidence as passing.
- Do not update product stability labels directly; downstream automation may do so only from `PASSED` attestations.

## Invocation Order

Run last, after `compare-three-engines`. A `FAILED` decision may trigger a separate repair cycle. A `BLOCKED_ENV` decision pauses until the exact missing dependency changes.
