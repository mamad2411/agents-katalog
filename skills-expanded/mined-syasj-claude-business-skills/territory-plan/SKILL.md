---
name: territory-plan
description: "Plan a territory from the accounts that fit, the capacity of the seller, and a weekly rhythm. Use when the user mentions territory plan, patch plan, account prioritization, sales coverage plan, or asks for a territory plan. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'territory-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Territory Plan

Plan a territory from the accounts that fit, the capacity of the seller, and a weekly rhythm.

## When to use this skill

Use this skill when the user:

- territory plan
- patch plan
- account prioritization
- sales coverage plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The account list
- Fit criteria
- Seller capacity
- Current pipeline already in motion

## Workflow


### 1. Fit

Define who belongs in the territory this quarter. A list of every logo is not a plan.
### 2. Tiers

A small number of accounts get a real plan. The rest get a lighter touch. Say the cut.
### 3. Capacity

Estimate time for existing deals before adding new logos. Do not overload the week and call it hustle.
### 4. Whitespace

Note where the user lacks coverage. Do not invent intent data.
### 5. Rhythm

Weekly actions the seller can finish. Inputs, not slogans.
### 6. Manager help

The one obstacle that needs manager air cover.

## Output

Deliver a **territory plan**.

- Purpose of this territory plan, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a territory plan by 30 September 2026. A rep has 200 accounts and ten hours a week for prospecting after live deals.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A rep has 200 accounts and ten hours a week for prospecting after live deals.

The account list: Harbor Goods; Cedar Clinic; Redline Parts
Fit criteria: their existing list, 6 lines. Two lines have no owner
Seller capacity: two people, no overtime figure
Current pipeline already in motion: the one named in the ask. Version and owner not recorded
```

### Example outcome

**Territory plan**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Fully works a small set, parks the rest, and fits the ten hours.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The account list | Harbor Goods; Cedar Clinic; Redline Parts | Needs confirmation |
| Fit criteria | their existing list, 6 lines. Two lines have no owner | Carried into the draft |
| Seller capacity | two people, no overtime figure | Carried into the draft |
| Current pipeline already in motion | the one named in the ask. Version and owner not recorded | Needs confirmation |

**How this draft was built**

**1. Fit**  
Define who belongs in the territory this quarter. A list of every logo is not a plan.

**2. Tiers**  
A small number of accounts get a real plan. The rest get a lighter touch. Say the cut.

**3. Capacity**  
Estimate time for existing deals before adding new logos. Do not overload the week and call it hustle.

**4. Whitespace**  
Note where the user lacks coverage. Do not invent intent data.

**5. Rhythm**  
Weekly actions the seller can finish. Inputs, not slogans.

**Deliberately not done**
- Equal time for every logo.
- A plan that ignores live deals.
- Invented buyer intent scores.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Equal time for every logo.
- A plan that ignores live deals.
- Invented buyer intent scores.

## Related skills

- `account-plan`
- `pipeline-review`
