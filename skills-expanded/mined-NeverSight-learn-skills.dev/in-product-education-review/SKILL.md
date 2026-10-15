---
name: in-product-education-review
description: Design and audit in-product education, onboarding checklists, tooltips, empty-state guidance, contextual help, tours, templates, examples, nudges, feature discovery, upgrade education, and help-center handoffs. Use when a product needs to teach users without cluttering UI, blocking expert workflows, or becoming spammy growth messaging.
---

# In Product Education Review

Use this skill to convert a risky product, operations, trust, or marketplace question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify user stage, job, confusion point, desired action, product surface, and existing help/support evidence.
2. Read `references/in-product-education-patterns.md`.
3. Map education type: checklist, tooltip, inline help, template, sample data, tour, empty state, coach mark, or help link.
4. Define trigger, dismissal, persistence, personalization, accessibility, metrics, and support/help-center handoff.
5. Produce education journey, content matrix, state flow, event schema, and cleanup plan.

## Guardrails

- Do not use education as a bandage for broken IA or unclear product copy.
- Do not interrupt expert users repeatedly after dismissal or completion.
- Do not hide upsell or dark-pattern nudges inside helpful education.
- Education must be accessible, localizable, and measurable by retained learning/action, not views alone.

## Output format

```text
Education context:
User stage / confusion / desired action:

Content matrix:
| Moment | Format | Trigger | Message | Dismissal | Metric |
| --- | --- | --- | --- | --- | --- |

State flow:
- <eligible/shown/used/dismissed/completed>

Quality checks:
- <accessibility/localization/support/product gap>
```
