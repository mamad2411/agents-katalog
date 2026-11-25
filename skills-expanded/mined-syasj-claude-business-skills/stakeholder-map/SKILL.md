---
name: stakeholder-map
description: "Map who can help or block a decision, and how to engage them without manipulation. Use when the user mentions stakeholder map, who do we need, political landscape, influence map, or asks for a stakeholder map and engagement plan. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'stakeholder-map' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Stakeholder Map

Map who can help or block a decision, and how to engage them without manipulation.

## When to use this skill

Use this skill when the user:

- stakeholder map
- who do we need
- political landscape
- influence map

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

- The decision or change
- People involved, as the user named them
- Known concerns
- The engagement the user is willing to do

## Workflow


### 1. List actors

Include operators, approvers, customers, and skeptics. Do not limit the map to people who already agree.
### 2. Assess influence and interest

Use the user's judgment. Do not psychoanalyze people or invent motives.
### 3. Write the concern

For each important actor, state the concern in language they would recognize.
### 4. Plan honest engagement

What they need to know, what you need from them, and when. No tricks, no concealed agendas.
### 5. Find the gap

Who has not been heard and could stop the work late. Late surprise is the failure mode this skill prevents.
### 6. Keep it private and respectful

Mark the map as internal. Do not write insults or personal rumors.

## Output

Deliver a **stakeholder map and engagement plan**.

- Purpose of this stakeholder map and engagement plan, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a stakeholder map and engagement plan by 30 September 2026. A plant manager wants to change the shift pattern and knows the union rep and two supervisors are uneasy.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A plant manager wants to change the shift pattern and knows the union rep and two supervisors are uneasy.

The decision or change: A plant manager wants to change the shift pattern and knows the union rep and two supervisors are uneasy
People involved, as the user named them: open item, last reviewed 14 September 2026. No owner named since
Known concerns: Bright Axle. Stated in the ask, not documented anywhere else
The engagement the user is willing to do: Harbor & Co, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Stakeholder map and engagement plan**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Does not hide the effect on hours.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision or change | A plant manager wants to change the shift pattern and knows the union rep and two supervisors are uneasy | Needs confirmation |
| People involved, as the user named them | open item, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Known concerns | Bright Axle. Stated in the ask, not documented anywhere else | Carried into the draft |
| The engagement the user is willing to do | Harbor & Co, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. List actors**  
Include operators, approvers, customers, and skeptics. Do not limit the map to people who already agree.

**2. Assess influence and interest**  
Use the user's judgment. Do not psychoanalyze people or invent motives.

**3. Write the concern**  
For each important actor, state the concern in language they would recognize.

**4. Plan honest engagement**  
What they need to know, what you need from them, and when. No tricks, no concealed agendas.

**5. Find the gap**  
Who has not been heard and could stop the work late. Late surprise is the failure mode this skill prevents.

**Deliberately not done**
- A map that is only the organizing committee.
- Engagement tactics that hide material facts.
- Invented personalities.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A map that is only the organizing committee.
- Engagement tactics that hide material facts.
- Invented personalities.

## Related skills

- `change-leadership`
- `stakeholder-update`
- `internal-comms-plan`
