---
name: forecast-accuracy
description: "Measure how forecasts missed, separate bias from noise, and change the forecasting habit rather than the template. Use when the user mentions forecast accuracy, why is the forecast always wrong, forecast bias, prediction error, or asks for a forecast accuracy review. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'forecast-accuracy' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Forecast Accuracy Review

Measure how forecasts missed, separate bias from noise, and change the forecasting habit rather than the template.

## When to use this skill

Use this skill when the user:

- forecast accuracy
- why is the forecast always wrong
- forecast bias
- prediction error

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not investment, tax, or financial advice. Do not invent rates of return, tax rates, or valuation multiples. A qualified finance professional must review any decision that moves money.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Prior forecasts and actuals
- The grain: week, month, product, or team
- Known one-off events
- Who owns the forecast

## Workflow


### 1. Choose the grain

Accuracy at the company level can hide a biased team. Use the grain the decision needs.
### 2. Measure error and bias

Direction matters. A forecast that is always high is a different problem from one that jumps around.
### 3. Exclude explained one-offs only if the user identifies them

Do not scrub the record to make the team look better.
### 4. Find the habit

Sandbagging, hockey sticks, or ignored pipeline. Recommend one habit change.
### 5. Do not add a new model first

If the inputs are political, a fancier model will be political too.
### 6. Set a review

Compare the next two cycles to this baseline and stop there.

## Output

Deliver a **forecast accuracy review**.

- Purpose of this forecast accuracy review, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a forecast accuracy review by 30 September 2026. Revenue forecasts have been high four months in a row and the team wants a new tool.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Revenue forecasts have been high four months in a row and the team wants a new tool.

Prior forecasts and actuals: plan 120, no second scenario attached
The grain: week, month, product, or team: week: in the file; month: not in the file; product: open; team: in the file
Known one-off events: Harbor & Co receipt. Stated in the ask, not documented anywhere else
Who owns the forecast: plan 120, no second scenario attached
```

### Example outcome

**Forecast accuracy review**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows the directional bias, names the habit, and delays a tooling recommendation until the habit changes.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Prior forecasts and actuals | plan 120, no second scenario attached | Needs confirmation |
| The grain: week, month, product, or team | week: in the file; month: not in the file; product: open; team: in the file | Carried into the draft |
| Known one-off events | Harbor & Co receipt. Stated in the ask, not documented anywhere else | Carried into the draft |
| Who owns the forecast | plan 120, no second scenario attached | Needs confirmation |

**How this draft was built**

**1. Choose the grain**  
Accuracy at the company level can hide a biased team. Use the grain the decision needs.

**2. Measure error and bias**  
Direction matters. A forecast that is always high is a different problem from one that jumps around.

**3. Exclude explained one-offs only if the user identifies them**  
Do not scrub the record to make the team look better.

**4. Find the habit**  
Sandbagging, hockey sticks, or ignored pipeline. Recommend one habit change.

**5. Do not add a new model first**  
If the inputs are political, a fancier model will be political too.

**Deliberately not done**
- A single MAPE number with no bias view.
- Deleting inconvenient misses.
- Buying software before fixing the habit.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A single MAPE number with no bias view.
- Deleting inconvenient misses.
- Buying software before fixing the habit.

## Related skills

- `budget-variance-review`
- `demand-plan-review`
- `pipeline-review`
