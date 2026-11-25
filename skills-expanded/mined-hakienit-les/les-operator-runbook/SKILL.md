---
name: les-operator-runbook
description: Write a bounded operational runbook for a repeatable maintenance, recovery, verification, or escalation procedure.
invocation: user
maturity: stable
route: operator-runbook
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/handoff-recovery.md","../../policies/risk-model.md","../../policies/rules/error-handling.md","../../policies/rules/documentation.md"]
---

# Operator Runbook

## Invoke

Bootstrap LES when a human or agent needs a repeatable operational procedure with
clear prerequisites, evidence, rollback, and escalation.

## Inputs

Operational objective, audience, prerequisites, observable signals, safe commands,
approval points, rollback, escalation owner, and expiry.

## Procedure

1. Define scope and entry conditions. Done when: the operator can tell whether the runbook applies.
2. Order safe inspection, action, and verification steps. Done when: every step has a completion signal and risk boundary.
3. Add failure, rollback, escalation, and stop paths. Done when: uncertainty cannot silently turn into a destructive action.
4. Exercise the runbook with a dry or read-only path. Done when: commands, paths, and evidence are current.

## Output

Runbook with prerequisites, steps, evidence, approvals, rollback, escalation,
expiry, and terminal status.

## Guardrails

Do not embed credentials or assume approval. Destructive or external steps stop at
the existing risk gate immediately before execution.

## Verification

Run the safest available proof, validate command paths, and mark live or unavailable
steps explicitly instead of claiming operational readiness.
