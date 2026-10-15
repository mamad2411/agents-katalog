---
name: platform-certification-program-review
description: Design and audit platform certification programs for partners, apps, plugins, integrations, agencies, creators, marketplace listings, templates, and developers. Covers eligibility, quality gates, test suites, badge policy, renewal, audits, appeals, revocation, partner enablement, directory ranking, and customer trust. Use when a platform needs reliable ecosystem quality signals.
---

# Platform Certification Program Review

Use this skill to convert a platform certification, partner/app/plugin quality gates, badges, renewal, audits, appeals, revocation, and ecosystem trust question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify ecosystem actor, certification promise, customer trust risk, eligibility criteria, test surface, badge value, renewal cadence, and enforcement owner.
2. Read `references/platform-certification-program-patterns.md`.
3. Classify program: integration certification, app/plugin review, agency partner tier, creator quality badge, template certification, or developer competency.
4. Define criteria, evidence, test harness, manual review, badge/display rules, directory effects, renewal, audit, appeal, revocation, and partner enablement.
5. Produce certification program plan, state machine, decision table, event schema, review checklist, and governance cadence.

## Guardrails

- Do not award badges whose meaning is unclear, untested, pay-to-win, or stale.
- Do not let certification bypass security, privacy, marketplace moderation, or customer-support readiness.
- Do not revoke certification without notice, evidence, appeal path, and customer-impact plan when stakes are high.
- Do not mix paid partner tiers with quality certification without labels and governance.

## Output format

```text
Certification context:
Actor / promise / criteria / customer trust risk:

Certification program plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Criteria, tests, and badges:
- <item> -> <policy, metric, edge case, support note>

Renewal, appeal, and revocation policy:
- <trigger> -> <action, communication, owner>
```
