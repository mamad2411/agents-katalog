---
name: cohort-analysis
description: "Build a cohort view that follows a defined group over time without mixing incompatible cohorts. Use when the user mentions cohort analysis, retention cohort, cohort curve, vintage analysis, or asks for a cohort analysis. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'cohort-analysis' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Cohort Analysis

Build a cohort view that follows a defined group over time without mixing incompatible cohorts.

## When to use this skill

Use this skill when the user:

- cohort analysis
- retention cohort
- cohort curve
- vintage analysis

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

- The cohort definition
- The event that starts the clock
- The success event
- The time grain

## Workflow


### 1. Step 1

Define membership and the start event before drawing a curve.
### 2. Step 2

Keep cohorts comparable. Do not mix a pricing change cohort into an older one without a label.
### 3. Step 3

Use only their data. If a week is incomplete, mark it incomplete rather than as a drop.
### 4. Step 4

Show the denominator. A retention rate without a cohort size is not interpretable.
### 5. Step 5

Call out mix shift if they supplied the evidence.
### 6. Step 6

Recommend one action or one next question. A curve alone is not a decision.

## Output

Deliver a **cohort analysis**.

- Purpose of this cohort analysis, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a cohort analysis by 30 September 2026. Last week's cohort looks like it retained worse, but the week is not over.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Last week's cohort looks like it retained worse, but the week is not over.

The cohort definition: orders_daily, recorded 14 September 2026. No supporting file attached
The event that starts the clock: orders_daily, recorded 14 September 2026. No supporting file attached
The success event: orders_daily, recorded 14 September 2026. No supporting file attached
The time grain: five working days, due 30 September 2026
```

### Example outcome

**Cohort analysis**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Marks the week incomplete and refuses a churn conclusion from it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The cohort definition | orders_daily, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The event that starts the clock | orders_daily, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The success event | orders_daily, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The time grain | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Define membership and the start event before drawing a curve**

**2. Keep cohorts comparable. Do not mix a pricing change cohort into an older one without a label**

**3. Use only their data. If a week is incomplete, mark it incomplete rather than as a drop**

**4. Show the denominator. A retention rate without a cohort size is not interpretable**

**5. Call out mix shift if they supplied the evidence**

**Deliberately not done**
- An incomplete week drawn as churn.
- No denominator.
- Mixing incompatible cohorts silently.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An incomplete week drawn as churn
- No denominator
- Mixing incompatible cohorts silently

## Related skills

- `funnel-analysis`
- `saas-metrics-pack`
