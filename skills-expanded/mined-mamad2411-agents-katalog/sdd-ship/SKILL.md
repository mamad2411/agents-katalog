---
name: sdd-ship
description: Use when review has no unresolved blocking findings and a completed SDD increment needs final acceptance verification and delivery readiness checks.
---

# SDD Ship

## Goal

Provide fresh evidence that the reviewed increment is ready for delivery.

## When to Use

Use after `sdd-review` has no unresolved `must-fix` findings and any `should-fix` finding is fixed or explicitly accepted.

Do not use to fix review findings.

## Prerequisites

Require the spec, plan, reviewed diff, and review outcome.

## Process

1. Map every acceptance criterion to implementation and evidence.
2. Rerun the necessary targeted verification.
3. Expand regression coverage according to interface, dependency, configuration, and shared-module risk.
4. Check for missing or uncommitted task changes.
5. Record commands, outcomes, unrun checks, and remaining risks.
6. Update an existing CHANGELOG when project convention and user-visible impact require it.
7. Create a CHANGELOG only when the user explicitly requests a format.

## Red Flags

- Reusing stale test results.
- Running an expensive full build without risk justification.
- Fixing code instead of returning to `sdd-build`.
- Introducing a changelog tool or format without project precedent.
- Pushing, releasing, or deploying without explicit instruction.

## Verification

Every acceptance criterion must have fresh, proportionate evidence. Explain any skipped check.

## Output

Use this heading structure. Do not rename top-level sections.

```markdown
# SDD Ship

## Acceptance Evidence

| Criterion | Implementation | Evidence (command + result) | Pass/Fail |
|-----------|---------------|----------------------------|-----------|
| AC-1      |               |                            |           |
| AC-2      |               |                            |           |

## Regression Checks

<!-- Verification beyond the scoped ACs: related modules, shared data, configuration. -->

- …

## Unrun Checks

<!-- Checks that were skipped and why (cost, risk, irrelevance). -->

- …

## Remaining Risks

<!-- Known gaps, accepted `should-fix` findings, or assumptions. -->

- …

## CHANGELOG

<!-- User-visible changes only, or "No CHANGELOG update needed." -->

## Delivery Status

<!-- What is ready and what remains as explicit user action (commit, push, PR, deploy). -->
```

Record only user-visible changes in CHANGELOG. Do not push, open a PR, publish, or deploy unless separately requested.

## Stop Conditions

Stop after the ship summary and any explicitly requested local commit. Do not push, open a PR, publish, or deploy unless separately requested.
