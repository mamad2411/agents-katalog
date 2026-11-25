---
name: thirty-sixty-ninety
description: "Write a 30-60-90 plan that a new hire and their manager can both grade. Use when the user mentions 30-60-90, ramp plan, first 90 days, new leader plan, or asks for a 30-60-90 plan. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'thirty-sixty-ninety' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Thirty Sixty Ninety Plan

Write a 30-60-90 plan that a new hire and their manager can both grade.

## When to use this skill

Use this skill when the user:

- 30-60-90
- ramp plan
- first 90 days
- new leader plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Role outcomes
- What the team most needs in the first quarter
- Known landmines
- How success will be judged

## Workflow


### 1. Step 1

30 days is learning and a small delivery: Relationships, system map, and one shipped contribution.
### 2. Step 2

60 days is independent work: The hire runs a defined slice without the manager in every step.
### 3. Step 3

90 days is a result: A measurable improvement or a decision the team needed. Not a list of meetings attended.
### 4. Manager commitments

What the manager will provide: context, introductions, and feedback dates.
### 5. Landmines

One or two risks the user named, and how the hire should treat them. No gossip section.
### 6. Review dates

Put the three reviews on the calendar in the plan itself.

## Output

Deliver a **30-60-90 plan**.

- Purpose of this 30-60-90 plan, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a 30-60-90 plan by 30 September 2026. A new team lead wants a 30-60-90 before day one, and the team has a late monthly close.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A new team lead wants a 30-60-90 before day one, and the team has a late monthly close.

Role outcomes: A new team lead wants a 30-60-90 before day one, and the team has a late monthly close. Stated once, in the ask. Not written down anywhere else
What the team most needs in the first quarter: two people on shift, one off
Known landmines: Sam Okonkwo. Stated in the ask, not documented anywhere else
How success will be judged: Sam Okonkwo, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**30-60-90 plan**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A plan whose 90-day result is a close improvement the manager can observe, with review dates included.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Role outcomes | A new team lead wants a 30-60-90 before day one, and the team has a late monthly close. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| What the team most needs in the first quarter | two people on shift, one off | Carried into the draft |
| Known landmines | Sam Okonkwo. Stated in the ask, not documented anywhere else | Carried into the draft |
| How success will be judged | Sam Okonkwo, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. 30 days is learning and a small delivery**  
Relationships, system map, and one shipped contribution.

**2. 60 days is independent work**  
The hire runs a defined slice without the manager in every step.

**3. 90 days is a result**  
A measurable improvement or a decision the team needed. Not a list of meetings attended.

**4. Manager commitments**  
What the manager will provide: context, introductions, and feedback dates.

**5. Landmines**  
One or two risks the user named, and how the hire should treat them. No gossip section.

**Deliberately not done**
- A 90-day plan that is only learning goals.
- No manager commitments.
- Unmeasurable 'build relationships' as the only 90-day result.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A 90-day plan that is only learning goals.
- No manager commitments.
- Unmeasurable 'build relationships' as the only 90-day result.

## Related skills

- `onboarding-plan`
- `performance-review`
- `manager-one-on-one`
