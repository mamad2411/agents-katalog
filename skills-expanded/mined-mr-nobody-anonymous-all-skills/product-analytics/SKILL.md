---
name: product-analytics
description: "Instrument and read product analytics: event taxonomy, funnel and retention definitions, cohort analysis, experiment measurement and warehouse-grade data quality."
type: procedural
category: product
domain: product
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - event tracking plan
  - product funnel analysis
  - retention cohort analysis
  - define activation metric
  - analytics instrumentation
aliases:
  - product-analytics
  - instrumentation
keywords:
  - analytics
  - events
  - funnel
  - retention
  - cohort
  - activation
  - taxonomy
mcp_servers:
  - postgres
  - bigquery
  - snowflake
source: custom
enabled: true
---

# Product Analytics

## Purpose

Instrument and read product analytics: event taxonomy, funnel and retention definitions, cohort analysis, experiment measurement and warehouse-grade data quality.

## When to Use

- Product decisions need behavioural evidence rather than opinion.
- Events are inconsistent and dashboards disagree.
- A funnel or retention claim must be defensible.

## When NOT to Use

- The product has no users yet.
- The question needs qualitative depth.
- The data pipeline cannot produce trustworthy joins.

## Capabilities

- Design a naming-conventioned event taxonomy with owners.
- Define activation, retention and churn precisely and consistently.
- Build funnels that handle timing and deduplication.
- Do cohort analysis without survivorship bias.
- Validate instrumentation with tests and audits.

## Inputs

- The critical user journeys to measure.
- Existing events and their known quality problems.
- The warehouse schema and identity resolution approach.

## Workflow

1. Write the taxonomy: object-action naming, required properties, owner per event.
2. Define each metric with numerator, denominator, window and exclusions.
3. Instrument, then verify with a test event through the real pipeline.
4. Build funnels per journey and sanity-check against raw counts.
5. Segment by cohort and acquisition source to avoid averaging away the signal.
6. Audit quarterly: unused events removed, drifting definitions corrected.

## Tools

- dbt
- bigquery
- amplitude
- posthog
- sql

## Examples

- `'Retention' without a window and an action is three different numbers in one meeting.`
- `Anonymous and logged-in ids must be stitched or the funnel loses every signup step.`

## Safety

- Collect the minimum personal data needed and document the lawful basis.
- Never build per-user surveillance dashboards without review.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |
| `bigquery` | stdio | full | high | `BIGQUERY_PROJECT`, `BIGQUERY_LOCATION`, `GOOGLE_APPLICATION_CREDENTIALS` |
| `snowflake` | stdio | full | high | `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/product/product-analytics`). First-party skill, maintained in this repository.

## Notes

- A metric definition belongs in version control, not in a slide.
- Instrument first, then design the dashboard around a decision.
- Pairs with: `user-research`, `conversion-rate-optimization`.
