---
name: enterprise-contract-redlines-review
description: Review enterprise contract redlines across liability, indemnity, privacy, data processing, security, SLA, support, uptime credits, payment terms, renewal, termination, audit rights, subprocessor, data residency, AI use, IP, confidentiality, order forms, and non-standard obligations. Use when commercial/legal changes could create product, finance, security, or operational commitments.
---

# Enterprise Contract Redlines Review

Use this skill to convert enterprise contract redlines, non-standard terms, legal/commercial risk, and operating-commitment questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify customer segment, deal value, redlined clause, requested obligation, standard fallback, affected systems, owner teams, and deadline.
2. Read `references/enterprise-contract-redlines-patterns.md`.
3. Classify redlines as acceptable fallback, commercial approval, legal review, security/privacy review, finance review, product capability gap, operational exception, or reject.
4. Define evidence, fallback language, approval owner, implementation/control requirement, expiry/review point, and customer response.
5. Produce redline review, state machine, decision table, event schema, approval checklist, and obligation handoff plan.

## Guardrails

- Do not accept contract language that promises controls, SLAs, data handling, support, or roadmap behavior the product cannot operate.
- Do not treat redlines as purely legal; route finance, security, privacy, support, product, and operations impacts to owners.
- Do not create hidden customer-specific obligations without source-of-truth tracking and renewal review.
- Do not provide legal advice; provide operating-risk analysis and route final language to approved legal/commercial owners.

## Output format

```text
Redline context:
Audience / source of truth / risk boundary:

Contract risk plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Fallbacks, approvals, obligations, and renewal review:
- <trigger> -> <policy, metric, edge case, support note>
```
