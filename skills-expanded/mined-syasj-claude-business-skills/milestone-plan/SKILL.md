---
name: milestone-plan
description: "Build a milestone plan from dependencies and evidence of done, not from evenly spaced dates. Use when the user mentions milestone plan, project timeline, phase plan, delivery plan, or asks for a milestone plan. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'milestone-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Milestone Plan

Build a milestone plan from dependencies and evidence of done, not from evenly spaced dates.

## When to use this skill

Use this skill when the user:

- milestone plan
- project timeline
- phase plan
- delivery plan

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

- The outcome
- Dependencies
- Real constraints on dates
- What done means for each milestone

## Workflow


### 1. Step 1

Define done for each milestone as evidence, not as a meeting.
### 2. Step 2

Sequence from dependencies. Do not spray dates evenly unless the work is actually even.
### 3. Step 3

Put external dependencies on the plan with owners.
### 4. Step 4

Include a buffer only if the user accepts one, and label it.
### 5. Step 5

Mark any date that is a wish rather than a commitment.
### 6. Step 6

Identify the milestone that will slip first if the top risk hits.

## Output

Deliver a **milestone plan**.

- Purpose of this milestone plan, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a milestone plan by 30 September 2026. A plan shows design, build, and test as three equal months with no dependency on a vendor.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A plan shows design, build, and test as three equal months with no dependency on a vendor.

The outcome: A plan shows design, build, and test as three equal months with no dependency on a vendor. Stated once, in the ask. Not written down anywhere else
Dependencies: RAID item 12 and one other, both unconfirmed as of 14 September 2026
Real constraints on dates: no extra headcount, and no result that is not in this file
What done means for each milestone: plain, for people who already know the context. No house guide attached
```

### Example outcome

**Milestone plan**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Places the vendor dependency, defines evidence of done, and labels uncommitted dates.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcome | A plan shows design, build, and test as three equal months with no dependency on a vendor. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Dependencies | RAID item 12 and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Real constraints on dates | no extra headcount, and no result that is not in this file | Carried into the draft |
| What done means for each milestone | plain, for people who already know the context. No house guide attached | Needs confirmation |

**How this draft was built**

**1. Define done for each milestone as evidence, not as a meeting**

**2. Sequence from dependencies. Do not spray dates evenly unless the work is actually even**

**3. Put external dependencies on the plan with owners**

**4. Include a buffer only if the user accepts one, and label it**

**5. Mark any date that is a wish rather than a commitment**

**Deliberately not done**
- Evenly spaced dates with no dependencies.
- A milestone that is only a meeting.
- Wish dates labeled as commitments.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Evenly spaced dates with no dependencies
- A milestone that is only a meeting
- Wish dates labeled as commitments

## Related skills

- `project-charter`
- `dependency-map`
