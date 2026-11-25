---
name: analytics-and-telemetry
version: 1.0.0
description: Instrumenting product usage data to validate business-value hypotheses — event design, funnel analysis, and avoiding vanity metrics. Load when designing what to track for a feature, or when interpreting usage data to validate a decision.
---

# Analytics & Telemetry

## Instrument against the hypothesis, not everything possible

Before adding tracking, state what question this data will answer and what decision it will inform — "track everything, figure out the question later" produces noise no one can act on and a privacy/data-minimization problem (see `privacy-engineering`) besides.

## Event design

Consistent naming and property schema across events — an inconsistent taxonomy makes cross-feature analysis unreliable. Track the action and its meaningful context (not raw clicks devoid of intent) so a funnel or cohort analysis is actually answerable later.

## Vanity vs. actionable metrics

A metric that goes up regardless of whether the product is actually working (page views, total signups with no activation) is vanity — prefer metrics tied to the outcome the feature was built for (task completion rate, retention, conversion at the specific step this feature affects).

## Funnel and cohort analysis

Track a full funnel (not just the entry and final conversion point) so a drop-off can be localized to the specific step losing users, and segment by cohort (new vs. returning, by acquisition channel) where behavior plausibly differs — an aggregate number can hide two very different populations behaving oppositely.

## Feeding back into product decisions

Analytics exists to validate or falsify a stated hypothesis from `product-manager`'s roadmap reasoning — report against that hypothesis explicitly, not just as a general dashboard update, and feed the result into `.claude/memory/<project>/vision.md`/`roadmap.md`.
