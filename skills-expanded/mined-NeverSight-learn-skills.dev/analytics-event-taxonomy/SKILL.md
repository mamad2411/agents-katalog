---
name: analytics-event-taxonomy
description: Design and audit analytics event taxonomies for product funnels, SaaS, mobile apps, games, web apps, desktop utilities, marketplaces, notifications, payments, support, and launches. Use when defining events, properties, naming, identity, funnels, cohorts, attribution, guardrail metrics, dashboards, or analytics quality rules.
---

# Analytics Event Taxonomy

Use this skill to make product analytics answer decisions instead of generating noisy events.

## Workflow

1. Identify product decisions, lifecycle funnel, entities, identity model, and instrumentation surfaces.
2. Read `references/analytics-event-taxonomy-patterns.md`.
3. Define event names, properties, identity, lifecycle stages, guardrail metrics, and QA checks.
4. Remove vanity or duplicate events.
5. Produce event taxonomy and validation plan.

## Guardrails

- Do not track sensitive data without purpose and privacy review.
- Do not create events without a decision they support.
- Keep names stable, semantic, and versioned when necessary.

## Output format

```text
Decision questions:
Identity model:

Event taxonomy:
- <event_name>: trigger, properties, owner, decision supported

Funnels/cohorts:
- <funnel or cohort>

Quality checks:
- <check>
```
