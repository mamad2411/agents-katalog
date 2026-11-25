---
name: retention-cohort-review
description: Analyze and improve retention cohorts for SaaS, mobile apps, games, developer tools, marketplaces, subscriptions, content products, and communities including activation cohorts, D1/D7/D30, weekly/monthly retention, rolling retention, resurrection, churn, segment bias, lifecycle events, monetization impact, cohort dashboards, and experiment readouts. Use when retention looks weak, confusing, misleading, or needs an action plan.
---

# Retention Cohort Review

Use this skill to turn retention charts into product decisions instead of dashboard theater.

## Workflow

1. Identify product loop, activation event, cohort definition, time grain, segment, and business model.
2. Read `references/retention-cohort-systems.md`.
3. Check whether the metric answers a decision: activation, habit, subscription renewal, content return, game progression, marketplace repeat, or developer production use.
4. Separate measurement errors, segment mix, acquisition quality, onboarding gaps, value gaps, lifecycle messaging, and monetization effects.
5. Produce a diagnosis, cohort cuts, event fixes, product hypotheses, and experiment plan.

## Guardrails

- Do not compare cohorts without controlling for acquisition source, platform, geography, version, seasonality, and activation state.
- Do not optimize short-term return if it increases fatigue, refunds, churn, or low-quality usage.
- Do not treat signup as activation unless signup is the product value.

## Output format

```text
Retention question:
Cohort definition:

Diagnosis:
- signal, evidence, caveat

Cohort cuts needed:
- <segment> -> why

Action plan:
- product change, metric, expected movement, guardrail

Instrumentation gaps:
- <event/property>
```
