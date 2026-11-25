---
name: demand-plan-review
description: "Review a demand plan for bias, assumptions, and the one driver that would change supply. Use when the user mentions demand plan, forecast review, demand review, S&OP demand, or asks for a demand plan review. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'demand-plan-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Demand Plan Review

Review a demand plan for bias, assumptions, and the one driver that would change supply.

## When to use this skill

Use this skill when the user:

- demand plan
- forecast review
- demand review
- S&OP demand

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Inventory and supplier recommendations depend on the user's lead times and service targets. Do not invent supplier performance.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The forecast
- Recent actuals
- Known events
- Who owns the number

## Workflow


### 1. Step 1

Compare the plan to recent actuals they supplied.
### 2. Step 2

Separate a one-time event from a run-rate change.
### 3. Step 3

State the assumption that moves supply the most.
### 4. Step 4

Do not invent a market growth rate.
### 5. Step 5

Recommend a bias note if the plan is always high or low in their history.
### 6. Step 6

Send the agreed number to supply with the assumption visible.

## Output

Deliver a **demand plan review**.

- Purpose of this demand plan review, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a demand plan review by 30 September 2026. The plan repeats last year's hockey stick and actuals have missed it three times.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

The plan repeats last year's hockey stick and actuals have missed it three times.

The forecast: plan 130, no second scenario attached
Recent actuals: Calgary-Edmonton lane. Partly documented: the what is written down, the who is not
Known events: Redline Parts. Stated in the ask, not documented anywhere else
Who owns the number: Diane Cho, supply lead
```

### Example outcome

**Demand plan review**
To: Diane Cho, supply lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Flag the bias and refuses to treat the hockey stick as the base.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The forecast | plan 130, no second scenario attached | Needs confirmation |
| Recent actuals | Calgary-Edmonton lane. Partly documented: the what is written down, the who is not | Carried into the draft |
| Known events | Redline Parts. Stated in the ask, not documented anywhere else | Carried into the draft |
| Who owns the number | Diane Cho, supply lead | Needs confirmation |

**How this draft was built**

**1. Compare the plan to recent actuals they supplied**

**2. Separate a one-time event from a run-rate change**

**3. State the assumption that moves supply the most**

**4. Do not invent a market growth rate**

**5. Recommend a bias note if the plan is always high or low in their history**

**Deliberately not done**
- A plan with no actuals comparison.
- An invented growth rate.
- A hidden bias.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A plan with no actuals comparison
- An invented growth rate
- A hidden bias

## Related skills

- `forecast-accuracy`
- `s-and-op`
