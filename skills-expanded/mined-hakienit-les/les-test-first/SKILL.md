---
name: les-test-first
description: Develop changed behavior through a failing observable check when a stable test seam exists.
invocation: model
maturity: stable
route: test-first
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/testing.md","../../policies/rules/coding-quality.md","../../policies/verification.md"]
---

# Test First

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the testing policy.

## Inputs

Changed behavior, stable test seam, and acceptance condition.

## Procedure

1. Choose a public behavior seam and define the exact acceptance. Done when: the test can observe the user-facing contract rather than implementation detail.
2. Write the smallest observable failing check and run it. Done when: it fails for the intended missing behavior, not a typo or setup error.
3. Implement only enough behavior to pass. Done when: the focused check is green without speculative modes.
4. Refactor while green and run the affected boundary. Done when: the regression proof and integration contract both pass.

## Output

Red-green proof and terminal status.

## Guardrails

Do not test implementation detail or claim a red check where no seam exists. If no
valid seam exists, record the architectural gap and an alternative characterization
instead of writing a tautological test.

## Verification

Record the red and green commands, failure reason, changed behavior, and affected
suite. State `SKIPPED` with alternative proof only when the correct seam is absent
or the project explicitly accepts a non-testable boundary.

Bootstrap LES. Choose the narrowest stable behavior seam, make one check fail for
the intended reason, implement the minimum behavior, then refactor while green.
Output the behavior and its regression proof. Stop and report when no valid seam
exists; verify both the focused check and affected integration boundary.
