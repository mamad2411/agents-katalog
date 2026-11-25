---
name: capacity-plan
description: "Plan capacity from demand and real throughput, and show the constraint before hiring or buying. Use when the user mentions capacity plan, do we have capacity, throughput plan, staffing versus demand, or asks for a capacity plan. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'capacity-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Capacity Plan

Plan capacity from demand and real throughput, and show the constraint before hiring or buying.

## When to use this skill

Use this skill when the user:

- capacity plan
- do we have capacity
- throughput plan
- staffing versus demand

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Demand they expect
- Current throughput
- The constraint
- Time horizon

## Workflow


### 1. Step 1

Define the unit of work and the horizon.
### 2. Step 2

Use their throughput, not an industry benchmark.
### 3. Name the constraint

people, a tool, a supplier, or a policy.
### 4. Step 4

Show the gap between demand and throughput in their units.
### 5. Options

smooth demand, remove a wait, or add capacity. Adding capacity is not the default if a wait is the constraint.
### 6. Step 6

State what would make the plan wrong.

## Output

Deliver a **capacity plan**.

- Purpose of this capacity plan, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a capacity plan by 30 September 2026. A team wants three hires because the queue is long, and approvals sit for two days.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A team wants three hires because the queue is long, and approvals sit for two days.

Demand they expect: 70 in the last period. No prior period attached, so no trend
Current throughput: 70 in the last period. No prior period attached, so no trend
The constraint: no extra headcount, and no result that is not in this file
Time horizon: 13 weeks
```

### Example outcome

**Capacity plan**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Tests the approval wait before treating hires as the answer.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Demand they expect | 70 in the last period. No prior period attached, so no trend | Needs confirmation |
| Current throughput | 70 in the last period. No prior period attached, so no trend | Carried into the draft |
| The constraint | no extra headcount, and no result that is not in this file | Carried into the draft |
| Time horizon | 13 weeks | Needs confirmation |

**How this draft was built**

**1. Define the unit of work and the horizon**

**2. Use their throughput, not an industry benchmark**

**3. Name the constraint**  
people, a tool, a supplier, or a policy.

**4. Show the gap between demand and throughput in their units**

**5. Options**  
smooth demand, remove a wait, or add capacity. Adding capacity is not the default if a wait is the constraint.

**Deliberately not done**
- An invented benchmark.
- Hiring as the only option.
- A plan with no unit of work.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An invented benchmark
- Hiring as the only option
- A plan with no unit of work

## Related skills

- `workforce-plan`
- `queue-health`
