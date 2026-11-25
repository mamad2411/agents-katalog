---
name: les-verification
description: Verify that existing work meets stated acceptance conditions without expanding scope.
invocation: model
maturity: stable
route: verification
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/verification.md","../../policies/verification.md","../../policies/rules/definition-of-done.md"]
---

# Verification

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the verification workflow.

## Inputs

Acceptance conditions, changed scope, and available checks.

## Procedure

1. Normalize acceptance into observable conditions and evidence classes. Done when: no condition lacks an owner or decisive check.
2. Select the lowest sufficient verification tier and escalate with risk. Done when: command, journey, environment, and expected signal are recorded.
3. Run checks focused-to-broad and preserve exact results. Done when: pass, fail, skipped, unavailable, and pending evidence are separate.
4. Inspect final diff, policy, package boundary, and residual risk. Done when: completion claim matches evidence and next action is explicit.

## Output

Verification record with pass, fail, skipped, and unavailable evidence.

## Guardrails

Do not expand implementation or turn unavailable checks into passes.

## Verification

End at proof and return a truthful terminal status.

Bootstrap LES, then load `../../policies/workflows/verification.md`,
`../../policies/verification.md`, and the definition-of-done rule. Map every
condition to a decisive check and report pass, fail, skipped, and unavailable
evidence. Stop after proof; verification does not authorize new behavior.
