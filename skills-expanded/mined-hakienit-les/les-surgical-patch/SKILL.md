---
name: les-surgical-patch
description: Apply a small behavior correction at the narrowest shared owner when surrounding behavior must remain unchanged.
invocation: model
maturity: stable
route: surgical-patch
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/bug-fixing.md","../../policies/rules/testing.md","../../policies/rules/error-handling.md","../../policies/rules/change-scope.md"]
---

# Surgical Patch

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the bug-fixing workflow.

## Inputs

Narrow regression, surrounding contract, and shared owner.

## Procedure

1. Trace every caller of the candidate owner. Done when: blast radius is known.
2. Add one regression proof. Done when: the defect is captured.
3. Change the narrowest shared owner. Done when: surrounding behavior remains proven.

## Output

Minimal correction, preservation proof, and terminal status.

## Guardrails

Do not use this route for an unbounded refactor or unrelated cleanup.

## Verification

Run regression and impacted caller checks; report skipped evidence honestly.

Bootstrap LES. Reproduce the defect, trace sibling callers, patch the shared cause,
and preserve unrelated behavior. Output one focused change and regression check.
Stop if the cause remains uncertain or the required fix crosses an unapproved
boundary; verify the original symptom and nearest sibling path.
