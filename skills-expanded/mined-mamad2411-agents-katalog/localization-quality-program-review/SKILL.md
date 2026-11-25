---
name: localization-quality-program-review
description: Plan and audit localization quality programs for mobile apps, games, SaaS, web, desktop, store listings, lifecycle messages, support content, legal copy, RTL, truncation, pluralization, cultural fit, in-context review, pseudo-localization, LQA, release gates, and market feedback. Use when translation must become launch-quality product experience.
---

# Localization Quality Program Review

Use this skill to convert localization quality, LQA, translation, in-context review, market fit, RTL, and release-gate questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify target markets, product surfaces, supported platforms, source readiness, string system, translation workflow, reviewers, legal/support content, release timeline, and market risk.
2. Read `references/localization-quality-program-patterns.md`.
3. Classify scope as launch localization, market expansion, ongoing release train, regulated copy, game/live-ops content, support localization, or store/listing localization.
4. Define pseudo-localization, glossary/style guide, translation memory, in-context review, functional LQA, cultural/legal review, accessibility/RTL checks, and release gates.
5. Produce localization QA plan, state machine, decision table, event schema, coverage checklist, and defect triage model.

## Guardrails

- Do not treat localization as string translation only; check layout, flows, market expectations, support, legal, and store assets.
- Do not ship unsupported languages in onboarding, billing, cancellation, privacy, or support paths.
- Do not ignore RTL, pluralization, gender, date/time/number/currency formats, truncation, and text expansion.
- Do not let machine translation or vendor delivery bypass in-context product validation for critical flows.

## Output format

```text
Localization quality context:
Audience / source of truth / risk boundary:

Localization QA plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Coverage, defects, and release gates:
- <trigger> -> <policy, metric, edge case, support note>
```
