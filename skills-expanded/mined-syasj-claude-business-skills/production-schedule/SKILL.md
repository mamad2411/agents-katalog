---
name: production-schedule
description: "Review a production schedule against capacity, materials, and the promise that will slip first. Use when the user mentions production schedule, finite schedule, what will we build, schedule review, or asks for a schedule review. Manufacturing and quality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: manufacturing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'production-schedule' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Production Schedule Review

Review a production schedule against capacity, materials, and the promise that will slip first.

## When to use this skill

Use this skill when the user:

- production schedule
- finite schedule
- what will we build
- schedule review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Quality and safety procedures are drafts for the site's quality system. Do not bypass a hold, calibration, or safety step.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Demand
- Capacity
- Material constraints
- Frozen window if any

## Workflow


### 1. Show the constraint

labor, machine, or material, from their facts.
### 2. Step 2

Do not schedule over the constraint and call it a plan.
### 3. Step 3

Honor a frozen window they have. Changes inside it need a named approver.
### 4. Step 4

Identify the customer promise that slips first.
### 5. Step 5

Recommend a sequence rule they can repeat, not a daily argument.
### 6. Step 6

Separate a plan from a wish list of every order.

## Output

Deliver a **schedule review**.

- Purpose of this schedule review, in two sentences.
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

Gus Moretti, plant manager at Redline Parts in Nisku, needs a schedule review by 30 September 2026. The schedule loads 120 hours into an 80-hour cell and the status is on time.

### Example data

```text
From: Gus Moretti, plant manager
Organization: Redline Parts, Nisku
Date: 14 September 2026
Needed by: 30 September 2026

The schedule loads 120 hours into an 80-hour cell and the status is on time.

Demand: 45 in the last period. No prior period attached, so no trend
Capacity: two people, no overtime figure
Material constraints: no extra headcount, and no result that is not in this file
Frozen window if any: two deals cited from memory. Neither has a written loss reason
```

### Example outcome

**Schedule review**
To: Gus Moretti, plant manager, Redline Parts
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Cuts or sequences to 80 hours and names the promise that moves.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Demand | 45 in the last period. No prior period attached, so no trend | Needs confirmation |
| Capacity | two people, no overtime figure | Carried into the draft |
| Material constraints | no extra headcount, and no result that is not in this file | Carried into the draft |
| Frozen window if any | two deals cited from memory. Neither has a written loss reason | Needs confirmation |

**How this draft was built**

**1. Show the constraint**  
labor, machine, or material, from their facts.

**2. Do not schedule over the constraint and call it a plan**

**3. Honor a frozen window they have. Changes inside it need a named approver**

**4. Identify the customer promise that slips first**

**5. Recommend a sequence rule they can repeat, not a daily argument**

**Deliberately not done**
- A schedule over known capacity.
- Silent changes inside a freeze.
- No view of the first slipped promise.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Gus Moretti by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A schedule over known capacity
- Silent changes inside a freeze
- No view of the first slipped promise

## Related skills

- `capacity-plan`
- `shortage-playbook`
