---
name: les-quality-audit
description: Audit an existing scope for maintainability, correctness risk, dead complexity, and missing proof without implementing changes.
invocation: user
maturity: stable
route: quality
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/review.md","../../policies/rules/coding-quality.md","../../policies/rules/testing.md","../../policies/rules/documentation.md","../../policies/rules/error-handling.md"]
---

# Quality Audit

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the review workflow.

## Inputs

Audit scope, comparison point, and applicable quality policy.

## Procedure

1. Inspect maintainability and correctness risks. Done when: evidence is collected.
2. Check dead complexity and missing proof. Done when: findings are actionable.
3. Report residual uncertainty. Done when: no-finding claims stay bounded.

## Output

Quality findings with severity, evidence, impact, and next action.

## Guardrails

Read-only; do not rewrite scope as an implementation request.

## Verification

Link each finding to an observed path and state unrun checks.

Bootstrap LES. Bound the audit, trace live paths, and report only evidence-backed
issues that affect correctness, change cost, or verification. Output ranked
findings with exact locations and the smallest remediation. Stay read-only; verify
that each finding is reachable and not merely a stylistic preference.
