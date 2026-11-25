# V37 Validation Protocol

Domain: Tools
Lifecycle: Intake
Owner: Vioxniv
Skill Type: Policy/Guardrail, Procedure

<aside>
🧩

This is an **Intake** skill. Complete Examples + Verification before promoting.

</aside>

## Summary

- Procedure for validating changes against V37 operational expectations (host-first, evidence-governed).

## When to Use (Triggers)

- Before merging changes that affect V37 host verification, orchestration, or operational safety
- When investigating a suspected regression in V37 behavior

## Inputs

- Change summary (PR/commit/patch)
- Target environment (local/dev/prod)
- Expected behavior and constraints

## Outputs

- Pass/fail decision
- Notes on deviations and required fixes

## Procedure / Steps

1. Identify the affected surface (runtime mode, host verification, diagnostics, infra assumptions).
2. Run relevant checks (unit/integration, linters, CI gates).
3. Verify behavior against documented operational invariants (no invented workflows).
4. Capture evidence (links to logs, diffs, failing checks) and summary findings.

## Guardrails

- Do not mark as validated without running at least one concrete verification step (tests/logs/checks).
- Prefer evidence-backed conclusions; if evidence is missing, document the unknowns.

## Examples

### Good

- “CI passed; host verification now enforces X; logs show Y; no regressions observed.”

### Bad

- “Looks fine” without running checks or citing evidence.

## Verification

- Confirm required checks are green (or explicitly document which checks were not run and why).

## Sources / Evidence (Optional)

- Link relevant docs, PRs, CI logs, and reference rows in **Evidence**.