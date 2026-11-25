---
name: accessibility-conformance-program-review
description: Design and audit accessibility conformance programs for apps, SaaS, websites, desktop software, games, marketplaces, and developer tools. Covers WCAG targets, VPAT/ACR, audits, assistive-tech testing, design systems, issue severity, ownership, remediation, release gates, procurement evidence, and customer communication. Use when accessibility needs durable governance beyond one-off audits.
---

# Accessibility Conformance Program Review

Use this skill to convert a accessibility conformance, WCAG targets, VPAT/ACR, assistive-tech testing, remediation, release gates, and governance question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify product surfaces, legal/procurement expectations, WCAG target, user workflows, current issues, owners, release cadence, and evidence needs.
2. Read `references/accessibility-conformance-program-patterns.md`.
3. Classify work as audit, remediation, design-system governance, release gate, procurement evidence, VPAT/ACR, training, or assistive-tech test plan.
4. Define scope, standards, severity, test matrix, owners, remediation SLA, exceptions, release gates, documentation, and customer response.
5. Produce conformance program plan, state machine, decision table, event schema, checklist, and remediation governance cadence.

## Guardrails

- Do not claim WCAG conformance, VPAT status, or accessibility readiness without scoped evidence and known exceptions.
- Do not rely only on automated scanners for keyboard, screen reader, cognitive, motion, focus, or workflow accessibility.
- Do not defer critical blockers that prevent core tasks for disabled users.
- Do not let design-system components drift without accessibility ownership and regression checks.

## Output format

```text
Accessibility context:
Surface / standard / evidence / release gate:

Conformance program plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Tests, issues, and owners:
- <item> -> <policy, metric, edge case, support note>

Exceptions and remediation governance:
- <trigger> -> <action, communication, owner>
```
