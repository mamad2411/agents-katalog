---
name: privacy-impact-assessment-review
description: Run privacy impact assessments for new features, data collection, analytics, AI processing, profiling, vendors, retention, consent, legal basis, minimization, sensitive data, children/regulated users, DSAR, cross-border transfer, security controls, mitigations, launch gates, and record keeping. Use when product changes may affect personal data or user trust.
---

# Privacy Impact Assessment Review

Use this skill to convert privacy impact assessment, data processing, minimization, legal basis, vendor, retention, and mitigation questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify feature scope, user groups, data collected, purpose, legal basis, vendors, AI/analytics use, retention, sharing, region, sensitive data, and user controls.
2. Read `references/privacy-impact-assessment-patterns.md`.
3. Classify processing as low-risk routine, consent-sensitive, vendor/subprocessor, AI/profiling, cross-border transfer, sensitive data, child/regulated, or high-risk DPIA-needed.
4. Define data map, minimization, notice/consent, access controls, retention/deletion, DSAR path, risk mitigations, launch gate, and record of decision.
5. Produce PIA report, state machine, decision table, event schema, risk checklist, and mitigation plan.

## Guardrails

- Do not collect personal data because it is convenient; tie each field to purpose, retention, and user value.
- Do not rely on consent, legitimate interest, or contract language without jurisdiction and context review.
- Do not ship AI/profiling, sensitive-data, or child/regulated-user processing without elevated review.
- Do not treat privacy review as a one-time launch checkbox when data flows, vendors, or purposes change.

## Output format

```text
PIA context:
Audience / source of truth / risk boundary:

Privacy assessment plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Risks, mitigations, and launch gates:
- <trigger> -> <policy, metric, edge case, support note>
```
