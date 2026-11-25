---
name: les-security-review
description: Review a change or boundary specifically for trust, permission, secret, and sensitive-data failures.
invocation: user
maturity: stable
route: trust-boundary
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/review.md","../../policies/risk-model.md","../../policies/rules/security.md","../../policies/rules/error-handling.md"]
---

# Security Review

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the security review policy.

## Inputs

Reviewed scope, trust boundaries, assets, and acceptance source.

## Procedure

1. Enumerate entrypoints and assets. Done when: trust boundaries are explicit.
2. Trace validation, authorization, storage, logging, and failure paths. Done when: reachable risks are evidenced.
3. Shape severity-ordered findings. Done when: mitigation is actionable.

## Output

Security findings or no-finding result with terminal status.

## Guardrails

Read-only unless separately authorized; never expose secrets in evidence.

## Verification

Each finding includes a reachable path, impact, and safe next action.

Bootstrap LES. Fix the reviewed scope, enumerate trust boundaries and assets, then
trace validation, authorization, storage, logging, and failure behavior. Output
severity-ordered findings with evidence and mitigation. Remain read-only unless a
fix is requested; verify every finding against a reachable path.
