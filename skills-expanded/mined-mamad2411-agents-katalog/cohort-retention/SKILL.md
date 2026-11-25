---
name: cohort-retention
description: Use when analyzing repeat behavior over time and the AI should clarify cohort logic, retention rule, cadence, and interpretation risks.
source: perlytics-skill
version: 1.0.0
---

# Cohort Retention

## Purpose

Analyze retention with explicit cohort logic so the result actually means something.

## When to use

Use this skill when:

- the question is about return behavior over time
- a team is using retention language loosely
- you need to compare cohorts, channels, or product changes

## When not to use

Do not use this skill when:

- the task is about a one-time conversion flow
- the return rule is not meaningful for the product or business model

## Required thinking discipline

- Define the cohort entry rule.
- Define the retained behavior.
- Define the time interval and retention horizon.
- Distinguish retention from reactivation and expansion.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. Define the entity: user, account, buyer, team, or merchant.
2. Define cohort membership.
3. Define retained behavior and return window.
4. Choose the horizon and cadence.
5. Compare cohorts across useful segments.
6. Interpret differences carefully with lifecycle context.

## Output format

- Cohort definition
- Retention definition
- Horizon and cadence
- Cohort comparison summary
- Segment differences
- Caveats and likely drivers

## Good example

> Cohort = first-paid-month account cohorts. Retention = account records at least one paid invoice in each subsequent month. Compare 6-month retention by acquisition channel.

## Bad example

> Retention is how many users keep using the product.

Why this is bad:

- cohort entry is missing
- return rule is missing
- time cadence is missing

## Practical notes

- Say whether you are showing classic retention, rolling retention, or returning activity.
- Be careful when product usage is irregular by design.

## Optional variants

- Marketplace businesses: distinguish buyer and seller retention.
- B2B SaaS: decide whether retention is user-level or account-level.
