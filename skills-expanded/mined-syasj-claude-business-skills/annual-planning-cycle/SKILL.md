---
name: annual-planning-cycle
description: "Design a planning calendar that connects strategy, money, and team capacity without a three-month planning fog. Use when the user mentions annual planning, planning calendar, budget season, how to run planning, or asks for a annual planning cycle. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'annual-planning-cycle' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Annual Planning Cycle

Design a planning calendar that connects strategy, money, and team capacity without a three-month planning fog.

## When to use this skill

Use this skill when the user:

- annual planning
- planning calendar
- budget season
- how to run planning

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

- Fiscal year dates
- Who must approve the plan
- Inputs that were late last year
- Non-negotiable constraints

## Workflow


### 1. Work backward from approval

Put the board or CEO decision date on the calendar first, then the drafts that must precede it.
### 2. Sequence the work

Strategy choices before budget numbers. Headcount after the bets, not before.
### 3. Limit rounds

Recommend two draft cycles, not an open-ended negotiation. Name what is frozen after each round.
### 4. Define inputs

Each function provides a short template, not a private spreadsheet format. Specify the owner and due date.
### 5. Integrate capacity

The plan is not done when the slides match. It is done when named people can carry the work.
### 6. Retrospective slot

Add a one-hour review of the planning process itself after approval, while the pain is fresh.

## Output

Deliver a **annual planning cycle**.

- Purpose of this annual planning cycle, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs an annual planning cycle by 30 September 2026. A COO wants next year's planning to finish before December instead of drifting into February.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A COO wants next year's planning to finish before December instead of drifting into February.

Fiscal year dates: 30 September 2026
Who must approve the plan: Mara Chen, founder
Inputs that were late last year: Bright Axle and one other, both unconfirmed as of 14 September 2026
Non-negotiable constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Annual planning cycle**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A backward calendar from the approval date, two draft rounds, required inputs, and an explicit capacity check.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Fiscal year dates | 30 September 2026 | Needs confirmation |
| Who must approve the plan | Mara Chen, founder | Carried into the draft |
| Inputs that were late last year | Bright Axle and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Non-negotiable constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Work backward from approval**  
Put the board or CEO decision date on the calendar first, then the drafts that must precede it.

**2. Sequence the work**  
Strategy choices before budget numbers. Headcount after the bets, not before.

**3. Limit rounds**  
Recommend two draft cycles, not an open-ended negotiation. Name what is frozen after each round.

**4. Define inputs**  
Each function provides a short template, not a private spreadsheet format. Specify the owner and due date.

**5. Integrate capacity**  
The plan is not done when the slides match. It is done when named people can carry the work.

**Deliberately not done**
- Starting with departmental wish lists.
- Six rounds of budget negotiation.
- A plan that ignores who will do the work.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Starting with departmental wish lists.
- Six rounds of budget negotiation.
- A plan that ignores who will do the work.

## Related skills

- `strategic-plan-builder`
- `budget-variance-review`
- `workforce-plan`
