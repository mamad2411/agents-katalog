---
name: war-room-brief
description: "Stand up a short-lived response when a serious business issue needs daily focus, without turning panic into a permanent process. Use when the user mentions war room, crisis brief, we have a serious issue, daily response plan, or asks for a war-room brief. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'war-room-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# War Room Brief

Stand up a short-lived response when a serious business issue needs daily focus, without turning panic into a permanent process.

## When to use this skill

Use this skill when the user:

- war room
- crisis brief
- we have a serious issue
- daily response plan

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

- What happened, in facts
- Who is affected
- Decisions needed in the next 48 hours
- Who is in charge

## Workflow


### 1. State the incident

Facts, time, impact, and what is still unknown. No blame paragraph at the top.
### 2. Set the objective

What 'stable' means in the next 48 hours. A war room without an objective becomes a standing meeting.
### 3. Assign roles

One owner, a decision maker, a communications owner, and a note taker. Everyone else is on call, not in the room.
### 4. List decisions

Only decisions that cannot wait. Park strategy redesign.
### 5. Plan communications

Who needs to know what, internally and externally, and what must be approved before it is said. Do not draft deceptive reassurance.
### 6. Set an end

A review point when the war room dissolves back into normal cadence.

## Output

Deliver a **war-room brief**.

- Purpose of this war-room brief, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a war-room brief by 30 September 2026. A key supplier missed a shipment and three major customers will stock out within a week.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A key supplier missed a shipment and three major customers will stock out within a week.

What happened, in facts: open item, last reviewed 14 September 2026. No owner named since
Who is affected: Mara Chen, founder
Decisions needed in the next 48 hours: A key supplier missed a shipment and three major customers will stock out within a week
Who is in charge: Mara Chen, founder
```

### Example outcome

**War-room brief**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A 48-hour brief with an owner, the decisions required today, a truthful customer message draft, and an end condition.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What happened, in facts | open item, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Who is affected | Mara Chen, founder | Carried into the draft |
| Decisions needed in the next 48 hours | A key supplier missed a shipment and three major customers will stock out within a week | Carried into the draft |
| Who is in charge | Mara Chen, founder | Needs confirmation |

**How this draft was built**

**1. State the incident**  
Facts, time, impact, and what is still unknown. No blame paragraph at the top.

**2. Set the objective**  
What 'stable' means in the next 48 hours. A war room without an objective becomes a standing meeting.

**3. Assign roles**  
One owner, a decision maker, a communications owner, and a note taker. Everyone else is on call, not in the room.

**4. List decisions**  
Only decisions that cannot wait. Park strategy redesign.

**5. Plan communications**  
Who needs to know what, internally and externally, and what must be approved before it is said. Do not draft deceptive reassurance.

**Deliberately not done**
- Inviting the whole company into the war room.
- Promising customers facts you do not have.
- Leaving the war room running for months.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Inviting the whole company into the war room.
- Promising customers facts you do not have.
- Leaving the war room running for months.

## Related skills

- `incident-response-coord`
- `stakeholder-update`
- `shortage-playbook`
