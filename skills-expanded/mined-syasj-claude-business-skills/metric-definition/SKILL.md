---
name: metric-definition
description: "Define a metric so two teams would compute the same number from the same source. Use when the user mentions define a metric, metric definition, what does this KPI mean, single source of truth metric, or asks for a metric definition. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'metric-definition' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Metric Definition

Define a metric so two teams would compute the same number from the same source.

## When to use this skill

Use this skill when the user:

- define a metric
- metric definition
- what does this KPI mean
- single source of truth metric

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent numbers. If a source file is missing, say so. Distinguish observation from inference. Do not re-identify private data to make a point.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision the metric serves
- The source table or report they trust
- Inclusion and exclusion rules they already use
- The owner

## Workflow


### 1. Step 1

Write the decision the metric is for before naming the metric.
### 2. Step 2

Define numerator, denominator, time window, and exclusions in words a new analyst can apply.
### 3. Step 3

Name the source. If two reports disagree, the definition is not done until one source is chosen.
### 4. Step 4

Record the known ways the metric can be gamed and add a counter-metric.
### 5. Step 5

Set an owner and a change process. Silent definition changes are a finding.
### 6. Step 6

If the baseline is unknown, say so. Do not invent one.

## Output

Deliver a **metric definition**.

- Purpose of this metric definition, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a metric definition by 30 September 2026. Sales and finance report different revenue for the same month and both call it bookings.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Sales and finance report different revenue for the same month and both call it bookings.

The decision the metric serves: plan 180, actual 75
The source table or report they trust: note from Noah Berger, 14 September 2026. No outside report
Inclusion and exclusion rules they already use: orders_daily is open. customers was raised verbally and never logged
The owner: Noah Berger, data lead
```

### Example outcome

**Metric definition**
Fieldnote · 14 September 2026 · Due 30 September 2026

**Decision**
Picks one source, writes the formula, and flags the other report as a reconciliation item.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Kite Freight | plan 180, actual 75 | Use | Both sides of the comparison are in the file |
| Bright Axle | score 62 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Write the decision the metric is for before naming the metric
2. Define numerator, denominator, time window, and exclusions in words a new analyst can apply
3. Name the source. If two reports disagree, the definition is not done until one source is chosen
4. Record the known ways the metric can be gamed and add a counter-metric
5. Set an owner and a change process. Silent definition changes are a finding

**Deliberately not done**
- A metric with no formula.
- Two teams using different sources without a note.
- An invented baseline.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Noah Berger attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- A metric with no formula
- Two teams using different sources without a note
- An invented baseline

## Related skills

- `data-dictionary`
- `executive-insight`
