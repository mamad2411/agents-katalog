---
name: conversion-rate-optimization
description: "Improve conversion with evidence: funnel diagnosis, hypothesis prioritisation, A/B test design and analysis, and guarding against false wins."
type: procedural
category: product
domain: product
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - improve conversion rate
  - ab test design sample size
  - funnel drop off analysis
  - cro hypothesis prioritization
  - ab test significance
aliases:
  - cro
  - conversion
keywords:
  - cro
  - conversion
  - ab-test
  - funnel
  - hypothesis
  - sample-size
  - uplift
mcp_servers:
  - postgres
  - playwright
  - bigquery
source: custom
enabled: true
---

# Conversion Rate Optimization

## Purpose

Improve conversion with evidence: funnel diagnosis, hypothesis prioritisation, A/B test design and analysis, and guarding against false wins.

## When to Use

- A funnel leaks traffic and the reason is unproven.
- A test result is being called a win without power analysis.
- Traffic exists but conversion is below the category baseline.

## When NOT to Use

- Traffic is too low to reach statistical power.
- The page has a functional defect that should simply be fixed.
- The change is a legal or compliance requirement.

## Capabilities

- Localise the drop with a funnel rather than a hunch.
- Write hypotheses as cause, change, expected effect, measurement.
- Size the test before running it, including MDE and duration.
- Analyse with the pre-registered metric and guard against peeking.
- Check for novelty effects and segment-level harm.

## Inputs

- Funnel data with consistent definitions.
- Current baseline conversion and traffic volume.
- The business constraint: revenue per visitor, support load, brand risk.

## Workflow

1. Map the funnel and find where the largest absolute drop sits.
2. Combine analytics with qualitative evidence to form a hypothesis.
3. Prioritise by expected impact, confidence and effort.
4. Compute sample size from baseline and minimum detectable effect.
5. Run to the pre-computed duration; do not stop on a good day.
6. Report the effect with an interval, plus guardrail metrics.

## Tools

- posthog
- optimizely
- playwright
- python

## Examples

- `A 2% baseline needs roughly 10k visitors per arm to detect a 0.5-point lift.`
- `Stopping a test the moment it crosses 95% inflates false positives dramatically.`

## Safety

- Never test dark patterns or hidden costs; the win is churn with delay.
- Respect consent: analytics and experiments need a lawful basis.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |
| `playwright` | stdio | standard | medium | — |
| `bigquery` | stdio | full | high | `BIGQUERY_PROJECT`, `BIGQUERY_LOCATION`, `GOOGLE_APPLICATION_CREDENTIALS` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/product/conversion-rate-optimization`). First-party skill, maintained in this repository.

## Notes

- Most CRO wins come from clarity and friction removal, not button colours.
- Segment results; a global flat result can hide a big win and a big loss.
- Pairs with: `product-analytics`, `user-research`.
