---
name: service-lane-plan
description: "Plan the lane so promised times match the techs and the parts on hand. Use when the user mentions service lane, promise time, shop capacity, lane plan, or asks for a lane plan. Automotive skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: automotive
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'service-lane-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Service Lane Plan

Plan the lane so promised times match the techs and the parts on hand.

## When to use this skill

Use this skill when the user:

- service lane
- promise time
- shop capacity
- lane plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not a repair procedure for safety-critical systems and not a recall determination. Do not invent defect rates or tell anyone to disable a safety feature.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Promise times
- Tech hours
- Parts status
- Jobs that are waiting on approval

## Workflow


### 1. Step 1

Add the hours they estimated.
### 2. Step 2

Compare to tech hours on shift.
### 3. Step 3

A job with parts missing gets no promise time.
### 4. Step 4

Waiting-on-approval does not take a bay.
### 5. Step 5

Do not pull a safety recall forward of a booked job unless they said to.
### 6. Step 6

Name the overflow.

## Output

Deliver a **lane plan**.

- Purpose of this lane plan, in two sentences.
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

Promised hours on today's board are 22. Two techs have 8 hours each. Three jobs, including RO 4418, have no parts. Two more are waiting on customer approval.

### Example data

```text
promised hours: 22
tech hours: 16
parts missing: RO 4418, RO 4422, RO 4430
waiting on approval: RO 4401, RO 4404
loaner: none free
```

### Example outcome

**Lane plan**
Work up to 16 hours. The 22-hour promise does not fit the shift.
Park 4418, 4422, and 4430. No parts, no promise time.
4401 and 4404 do not take a bay until the customer approves.
No loaner is offered. None is free.
Overflow: Carla calls the three parts-missing customers. She does not pull a recall ahead of a booked job. Nobody asked for that.

## Anti-patterns

- Promise times that exceed the shift
- A bay held for an unapproved job
- A made-up efficiency rate

## Related skills

- `dealer-morning-review`
- `parts-backorder-note`
