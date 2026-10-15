---
name: compliance-audit-readiness-review
description: Prepare and audit compliance readiness for SOC 2, ISO 27001, GDPR, HIPAA-adjacent, procurement, internal controls, policy evidence, control owners, auditor requests, sampling, walkthroughs, exceptions, remediation, report claims, and renewal cadence. Use when teams need audit-ready evidence without inventing compliance claims.
---

# Compliance Audit Readiness Review

Use this skill to convert compliance audit readiness, controls, evidence, sampling, auditor request, exception, and remediation questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify audit framework, scope, period, systems, controls, control owners, evidence sources, auditor timeline, gaps, customer commitments, and trust-center dependencies.
2. Read `references/compliance-audit-readiness-patterns.md`.
3. Classify work as audit scoping, control mapping, evidence collection, walkthrough prep, sample response, exception remediation, report review, or continuous compliance.
4. Define control matrix, evidence calendar, owner accountability, request workflow, sampling response, gap register, remediation SLA, claim approval, and renewal cadence.
5. Produce audit readiness plan, state machine, decision table, event schema, evidence checklist, and risk/escalation register.

## Guardrails

- Do not claim certifications, attestations, control operation, or compliance status without approved evidence and owner/legal review.
- Do not collect audit evidence ad hoc at deadline when controls should operate continuously.
- Do not alter evidence, logs, screenshots, tickets, or timestamps to satisfy an auditor request.
- Do not let customer promises, security questionnaires, trust center claims, and audit reports drift apart.

## Output format

```text
Audit readiness context:
Audience / source of truth / risk boundary:

Audit readiness plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Controls, evidence, and remediation:
- <trigger> -> <policy, metric, edge case, support note>
```
