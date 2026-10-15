---
name: enterprise-security-exception-review
description: Design and audit enterprise security exception workflows covering customer security requirements, compensating controls, risk acceptance, expiry, evidence, owner approval, contract commitments, product gaps, supportability, escalation, renewal impact, and remediation tracking. Use when an enterprise buyer asks for a security exception or deviation from standard controls.
---

# Enterprise Security Exception Review

Use this skill to convert enterprise security exception, compensating control, customer requirement, risk acceptance, expiry, and remediation questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify customer request, control requirement, current standard, gap, affected data, contract impact, compensating controls, owner, expiry need, and remediation feasibility.
2. Read `references/enterprise-security-exception-patterns.md`.
3. Classify exception as no-exception-needed, documentation gap, customer-specific config, compensating control, risk acceptance, roadmap request, contract redline, or non-acceptable risk.
4. Define approval owner, evidence, compensating control, customer communication, expiry, renewal review, remediation plan, and support/runbook impact.
5. Produce exception review, state machine, decision table, event schema, risk checklist, and customer response plan.

## Guardrails

- Do not grant indefinite customer-specific security exceptions without owner, expiry, and renewal review.
- Do not let sales promise security controls, certifications, encryption, residency, logging, SSO, or retention exceptions without evidence.
- Do not accept exceptions that silently weaken other customers, shared infrastructure, or regulatory commitments.
- Do not confuse roadmap intent with currently operating compensating controls.

## Output format

```text
Security exception context:
Audience / source of truth / risk boundary:

Exception decision plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Compensating controls, expiry, and remediation:
- <trigger> -> <policy, metric, edge case, support note>
```
