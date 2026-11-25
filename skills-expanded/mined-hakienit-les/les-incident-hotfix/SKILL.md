---
name: les-incident-hotfix
description: Contain active production impact or urgent risk with the smallest reversible mitigation.
invocation: model
maturity: stable
route: incident
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/incident-hotfix.md","../../policies/risk-model.md","../../policies/rules/security.md","../../policies/rules/error-handling.md"]
---

# Incident Hotfix

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the incident workflow.

## Inputs

Verified impact, incident authority, and reversible mitigation options.

## Procedure

1. Confirm impact and preserve evidence. Done when: blast radius is known.
2. Select the smallest reversible mitigation. Done when: rollback is ready.
3. Verify the critical journey. Done when: mitigation evidence is recorded.

## Output

Mitigation record, rollback state, and follow-up boundary.

## Guardrails

Urgency never grants R3 authority or suppresses evidence.

## Verification

Return critical-journey and rollback results with terminal status.

Bootstrap LES. Confirm incident authority and impact, preserve evidence, select a
reversible containment, and keep follow-up repair separate. Output mitigation,
rollback, critical-journey evidence, and residual risk. Stop immediately before
external mutation without R3 approval; verify containment and rollback readiness.
