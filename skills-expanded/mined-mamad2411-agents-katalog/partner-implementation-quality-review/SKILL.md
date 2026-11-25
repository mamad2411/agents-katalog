---
name: partner-implementation-quality-review
description: Design and audit partner implementation quality across implementation partners, systems integrators, migration partners, onboarding partners, scopes of work, training, certification, customer acceptance, QA evidence, defects, support handoffs, security, data migration, integration quality, renewal impact, and partner scorecards. Use when partner-delivered work affects customer outcomes and product reputation.
---

# Partner Implementation Quality Review

Use this skill to convert partner implementation quality, systems integrator QA, migration partner review, onboarding partner acceptance, certification, partner scorecard, and customer handoff questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify partner type, customer scope, statement of work, implementation tasks, quality gates, data/integration risk, acceptance criteria, support handoff, scorecard, and remediation owner.
2. Read `references/partner-implementation-quality-patterns.md`.
3. Classify the situation as implementation kickoff, migration delivery, integration delivery, training delivery, QA checkpoint, customer acceptance, defect remediation, certification renewal, or partner performance review.
4. Define quality standards, evidence requirements, acceptance tests, customer signoff, defect triage, support handoff, scorecard metrics, remediation, and certification consequences.
5. Produce partner implementation quality plan, state machine, decision table, event schema, QA checklist, customer acceptance plan, and partner scorecard.

## Guardrails

- Do not let partner delivery quality be judged only by project completion or partner self-report.
- Do not accept migrations, integrations, permissions, or training without customer workflow validation.
- Do not hide partner-caused defects from support, customer success, product, or certification decisions.
- Do not certify or promote partners without recurring evidence and revocation criteria.

## Output format

```text
Partner implementation context:
Audience / source of truth / risk boundary:

Implementation quality plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Scope, QA evidence, customer acceptance, defects, handoff, scorecard, and certification:
- <trigger> -> <policy, metric, edge case, support note>
```
