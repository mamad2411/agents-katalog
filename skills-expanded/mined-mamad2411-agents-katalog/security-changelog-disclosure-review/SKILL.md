---
name: security-changelog-disclosure-review
description: Design and audit security changelog and disclosure operations covering vulnerability severity, exploitability, affected versions, remediation status, customer impact, trust center updates, release notes, CVE or advisory decisions, embargoes, legal review, support macros, detection guidance, timelines, and post-disclosure monitoring. Use when security-relevant changes need transparency without creating avoidable risk.
---

# Security Changelog Disclosure Review

Use this skill to convert security changelog, vulnerability disclosure, advisory, release notes, trust center update, customer security notification, embargo, and remediation-timeline questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify security change, affected versions, severity, exploitability, remediation state, customer exposure, disclosure audience, legal/security owner, embargo constraints, and support impact.
2. Read `references/security-changelog-disclosure-patterns.md`.
3. Classify the situation as routine hardening, dependency update, vulnerability fix, customer-impacting advisory, incident-related disclosure, CVE coordination, trust center update, or embargoed disclosure.
4. Define severity language, affected scope, mitigation, upgrade path, customer notice, release-note wording, support macro, trust center update, monitoring, and post-disclosure review.
5. Produce security disclosure plan, state machine, decision table, event schema, disclosure checklist, customer message, and monitoring plan.

## Guardrails

- Do not publish exploit-enabling details before mitigation, customer notice, or coordinated disclosure readiness.
- Do not bury customer-impacting security fixes in vague release notes that prevent customers from acting.
- Do not overstate severity, compliance status, affected scope, or remediation completeness.
- Do not let security, legal, support, sales, and trust-center messaging diverge.

## Output format

```text
Security disclosure context:
Audience / source of truth / risk boundary:

Security changelog plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Severity, scope, wording, customer action, trust center, and monitoring:
- <trigger> -> <policy, metric, edge case, support note>
```
