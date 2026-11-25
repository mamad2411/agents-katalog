---
name: north-star-metric
description: "Choose one north-star metric that reflects customer value, plus a handful of input metrics the team can move. Use when the user mentions north star metric, one metric that matters, company metric, what should we optimize, or asks for a north-star metric definition. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'north-star-metric' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# North Star Metric

Choose one north-star metric that reflects customer value, plus a handful of input metrics the team can move.

## When to use this skill

Use this skill when the user:

- north star metric
- one metric that matters
- company metric
- what should we optimize

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- How the customer gets value
- Current candidate metrics and their definitions
- Known ways the metric could be gamed
- Who will own it

## Workflow


### 1. Start from value

The north star should move when customers get value, not merely when the company books activity.
### 2. Reject vanity

Signups, page views, and raw revenue are usually poor north stars unless the user can show they match value in this business.
### 3. Write the definition

Numerator, denominator, inclusion rules, and source. A metric without a definition will be argued every week.
### 4. Add inputs

Three to five input metrics a team can influence this month. The north star is a result, not a lever.
### 5. Name the gaming risk

How a team could hit the number and hurt the customer. Add a counter-metric.
### 6. Do not worship it

State what the north star does not measure, so finance and quality concerns are not erased.

## Output

Deliver a **north-star metric definition**.

- Purpose of this north-star metric definition, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a north-star metric definition by 30 September 2026. A marketplace is debating GMV versus successful jobs completed as the company metric.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A marketplace is debating GMV versus successful jobs completed as the company metric.

How the customer gets value: Lantern Inn, last reviewed 14 September 2026. No owner named since
Current candidate metrics and their definitions: plan 120, actual 80
Known ways the metric could be gamed: plan 120, actual 80
Who will own it: Mara Chen, founder
```

### Example outcome

**North-star metric definition**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
A definition of the chosen metric, why the alternative loses, three input metrics, and a counter-metric that protects quality.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Redline Parts | plan 120, actual 80 | Use | Both sides of the comparison are in the file |
| Lantern Inn | score 78 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Start from value
2. Reject vanity
3. Write the definition
4. Add inputs
5. Name the gaming risk

**Deliberately not done**
- Picking revenue because it is easy to explain to a board.
- A north star with no definition.
- No counter-metric, so the number can be gamed.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Mara Chen attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- Picking revenue because it is easy to explain to a board.
- A north star with no definition.
- No counter-metric, so the number can be gamed.

## Related skills

- `okrs-and-scorecard`
- `metric-definition`
- `product-analytics-spec`
