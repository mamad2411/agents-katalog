---
name: sprint-plan
description: "Plan a sprint from capacity and a clear sprint goal, not from whoever added tickets last. Use when the user mentions sprint plan, plan the sprint, sprint goal, iteration plan, or asks for a sprint plan. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sprint-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sprint Plan

Plan a sprint from capacity and a clear sprint goal, not from whoever added tickets last.

## When to use this skill

Use this skill when the user:

- sprint plan
- plan the sprint
- sprint goal
- iteration plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Delivery plans are commitments only when owners and dates are real. Do not fabricate status to make a report look healthy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Team capacity
- Candidate work
- The sprint goal
- Known absences

## Workflow


### 1. Step 1

Write one sprint goal that a stakeholder can understand.
### 2. Step 2

Subtract absences from capacity before pulling work.
### 3. Step 3

Pull work that serves the goal until capacity is full. Park the rest visibly.
### 4. Step 4

Each selected item needs a done statement.
### 5. Step 5

Name dependencies that sit outside the team.
### 6. Step 6

Do not fill the sprint with unestimated 'small' work that has no owner.

## Output

Deliver a **sprint plan**.

- Purpose of this sprint plan, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a sprint plan by 30 September 2026. A team plans a full sprint while two people are out and the board is already full.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A team plans a full sprint while two people are out and the board is already full.

Team capacity: two people on shift, one off
Candidate work: 30 September 2026
The sprint goal: A team plans a full sprint while two people are out and the board is already full. Stated once, in the ask. Not written down anywhere else
Known absences: RAID item 12. Stated in the ask, not documented anywhere else
```

### Example outcome

**Sprint plan**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Cuts scope to the remaining capacity and states one goal.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Team capacity | two people on shift, one off | Needs confirmation |
| Candidate work | 30 September 2026 | Carried into the draft |
| The sprint goal | A team plans a full sprint while two people are out and the board is already full. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Known absences | RAID item 12. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Write one sprint goal that a stakeholder can understand**

**2. Subtract absences from capacity before pulling work**

**3. Pull work that serves the goal until capacity is full. Park the rest visibly**

**4. Each selected item needs a done statement**

**5. Name dependencies that sit outside the team**

**Deliberately not done**
- A sprint with no goal.
- Ignoring absences.
- A plan over capacity.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A sprint with no goal
- Ignoring absences
- A plan over capacity

## Related skills

- `definition-of-done`
- `estimation-review`
