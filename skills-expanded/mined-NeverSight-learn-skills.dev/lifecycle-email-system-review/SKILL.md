---
name: lifecycle-email-system-review
description: Design and audit lifecycle email systems for onboarding, activation, education, retention, winback, billing, product updates, community, marketplace, and transactional messaging. Covers segmentation, consent, suppression, deliverability, frequency caps, triggers, personalization, localization, measurement, and support handoff. Use when email should drive product outcomes without spam or trust damage.
---

# Lifecycle Email System Review

Use this skill to convert a lifecycle email, segmentation, consent, deliverability, suppression, triggers, personalization, and product outcomes question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify user journey, message purpose, consent basis, segment, trigger, sender reputation, localization, suppression rules, and success metric.
2. Read `references/lifecycle-email-system-patterns.md`.
3. Classify message as transactional, onboarding, activation, education, retention, winback, billing, trust/safety, community, or marketing campaign.
4. Define audience, trigger, eligibility, suppression, cadence, content, deliverability checks, unsubscribe/preference behavior, event tracking, and support fallback.
5. Produce lifecycle email plan, state machine, decision table, event schema, QA checklist, and fatigue-control policy.

## Guardrails

- Do not send marketing or winback emails without consent, suppression, unsubscribe, and preference handling.
- Do not mix transactional necessity with promotional content in ways that undermine compliance or trust.
- Do not optimize opens/clicks without activation, retention, refund, complaint, and unsubscribe guardrails.
- Do not keep emailing users after churn, deletion, region restrictions, or support opt-out without explicit policy.

## Output format

```text
Lifecycle email context:
Journey / consent / trigger / deliverability risk:

Lifecycle email plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Segments, triggers, and suppression:
- <item> -> <policy, metric, edge case, support note>

Fatigue and compliance policy:
- <trigger> -> <action, communication, owner>
```
