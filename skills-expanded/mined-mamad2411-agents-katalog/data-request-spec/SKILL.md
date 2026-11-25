---
name: data-request-spec
description: Use when analysis requires new data pulls, modeling, instrumentation, or dashboard changes and the AI should create a precise request specification.
source: perlytics-skill
version: 1.0.0
---

# Data Request Spec

## Purpose

Convert a business-analysis ask into a precise request that downstream data teams can execute without guesswork.

## When to use

Use this skill when:

- you need a new data extract
- you need a modeled table, event, or dashboard change
- the business ask is too vague for implementation

## When not to use

Do not use this skill when:

- the needed dataset already exists and is documented
- the work can be completed directly without a handoff

## Required thinking discipline

- Write for the builder, not the requester.
- Make metric definitions and grain explicit.
- Include acceptance criteria.
- Distinguish must-have fields from nice-to-have fields.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. State the business question and consumer.
2. Define the exact output needed.
3. Specify metric definitions and field requirements.
4. Specify grain, timeframe, and filters.
5. State delivery format and deadline.
6. Add acceptance criteria and assumptions.

## Output format

- Request summary
- Business purpose
- Required output
- Definitions
- Field list
- Grain, timeframe, filters
- Priority and deadline
- Acceptance criteria
- Assumptions and risks

## Good example

> Need a weekly account-level table for newly activated workspaces with activation source, first value event date, and 8-week retention flags, excluding internal and test accounts. Used by growth PM for onboarding analysis.

## Bad example

> Please pull retention data for onboarding.

Why this is bad:

- output shape is missing
- entity and timeframe are missing
- the downstream team must guess the business need

## Practical notes

- Include sample output columns when useful.
- If the request is exploratory, say so and narrow the v1 ask anyway.

## Optional variants

- Dashboard request: add KPI definitions and visualization expectations.
- Instrumentation request: add event naming and trigger conditions.
