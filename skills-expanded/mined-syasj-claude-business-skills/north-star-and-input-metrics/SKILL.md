---
name: north-star-and-input-metrics
description: "Define a product outcome metric and the input metrics a team can move this month. Use when the user mentions product metrics, input metrics, activation metric, product KPI, or asks for a product metric tree. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'north-star-and-input-metrics' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Product Metric Tree

Define a product outcome metric and the input metrics a team can move this month.

## When to use this skill

Use this skill when the user:

- product metrics
- input metrics
- activation metric
- product KPI

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The user value moment
- Candidate metrics and definitions
- What the team can change
- Known ways to game the metric

## Workflow


### 1. Value moment

The observable moment the user gets value. Registration is rarely that moment.
### 2. Definition

Numerator, denominator, and source. No definition, no metric.
### 3. Inputs

Three metrics the team can move with product work this month.
### 4. Counter-metric

The quality or cost signal that keeps the main metric honest.
### 5. Gaming

How a team could hit the number and hurt the user. Close that door in the definition.
### 6. Baseline

Use their baseline or mark it unknown. Do not invent one.

## Output

Deliver a **product metric tree**.

- Purpose of this product metric tree, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Jonah Park, product manager at Fieldnote in Edmonton, needs a product metric tree by 30 September 2026. A team wants to optimize signups, but activated users are the ones who finish a first export.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to optimize signups, but activated users are the ones who finish a first export.

The user value moment: Activation checklist, recorded 14 September 2026. No supporting file attached
Candidate metrics and definitions: plan 120, actual 80
What the team can change: two people on shift, one off
Known ways to game the metric: plan 120, actual 80
```

### Example outcome

**Product metric tree**
Fieldnote · 14 September 2026 · Due 30 September 2026

**Decision**
Uses the first successful export as the value moment and signups as a funnel input, with a failure counter-metric.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Redline Parts | plan 120, actual 80 | Use | Both sides of the comparison are in the file |
| Lantern Inn | score 78 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Value moment
2. Definition
3. Inputs
4. Counter-metric
5. Gaming

**Deliberately not done**
- Signups as the value metric by default.
- No counter-metric.
- An invented baseline.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Jonah Park attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- Signups as the value metric by default.
- No counter-metric.
- An invented baseline.

## Related skills

- `north-star-metric`
- `product-analytics-spec`
