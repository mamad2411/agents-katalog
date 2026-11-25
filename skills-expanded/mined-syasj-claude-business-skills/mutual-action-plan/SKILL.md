---
name: mutual-action-plan
description: "Draft a mutual action plan that shows the buyer's steps and the seller's steps on one timeline. Use when the user mentions mutual action plan, close plan, MAP, joint evaluation plan, or asks for a mutual action plan. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'mutual-action-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Mutual Action Plan

Draft a mutual action plan that shows the buyer's steps and the seller's steps on one timeline.

## When to use this skill

Use this skill when the user:

- mutual action plan
- close plan
- MAP
- joint evaluation plan

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

- The buyer's process steps
- Dates they have acknowledged
- Owners on both sides
- Open risks

## Workflow


### 1. Buyer steps first

Their legal, security, and business reviews. If you do not know them, the plan is a seller fantasy. Mark unknowns.
### 2. Dates

Only dates someone has agreed. Proposed dates are labeled proposed.
### 3. Owners

A named human on both sides for each step. 'Customer team' is not an owner.
### 4. Exit criteria

What done means for security review, pilot, or paper.
### 5. Risks

The step most likely to slip, and the question that would reveal it this week.
### 6. Tone

A shared project plan, not a pressure schedule. No fake deadlines.

## Output

Deliver a **mutual action plan**.

- Purpose of this mutual action plan, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a mutual action plan by 30 September 2026. A seller wants a mutual action plan, but the buyer has not named a security reviewer.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A seller wants a mutual action plan, but the buyer has not named a security reviewer.

The buyer's process steps: email to Samir Qureshi. No written steps after 1 Sep 2026
Dates they have acknowledged: 30 September 2026
Owners on both sides: Samir Qureshi, account executive
Open risks: Harbor Goods is open. No score in the file
```

### Example outcome

**Mutual action plan**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Leaves security review unowned and refuses to print a close date as agreed.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The buyer's process steps | email to Samir Qureshi. No written steps after 1 Sep 2026 | Needs confirmation |
| Dates they have acknowledged | 30 September 2026 | Carried into the draft |
| Owners on both sides | Samir Qureshi, account executive | Carried into the draft |
| Open risks | Harbor Goods is open. No score in the file | Needs confirmation |

**How this draft was built**

**1. Buyer steps first**  
Their legal, security, and business reviews. If you do not know them, the plan is a seller fantasy. Mark unknowns.

**2. Dates**  
Only dates someone has agreed. Proposed dates are labeled proposed.

**3. Owners**  
A named human on both sides for each step. 'Customer team' is not an owner.

**4. Exit criteria**  
What done means for security review, pilot, or paper.

**5. Risks**  
The step most likely to slip, and the question that would reveal it this week.

**Deliberately not done**
- A close plan with only seller tasks.
- Dates the buyer never acknowledged.
- Using the plan as a pressure tactic.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A close plan with only seller tasks.
- Dates the buyer never acknowledged.
- Using the plan as a pressure tactic.

## Related skills

- `qualification-meddic`
- `deal-desk-review`
