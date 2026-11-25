---
name: meeting-operating-system
description: "Redesign a meeting so it produces a decision or a documented exception, or cancel it. Use when the user mentions meeting redesign, too many meetings, operating review, meeting system, or asks for a meeting system. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'meeting-operating-system' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Meeting Operating System

Redesign a meeting so it produces a decision or a documented exception, or cancel it.

## When to use this skill

Use this skill when the user:

- meeting redesign
- too many meetings
- operating review
- meeting system

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

- The meeting's supposed purpose
- Who attends
- What decisions stall
- The pre-read if any

## Workflow


### 1. Step 1

Write the decision the meeting exists to make. If there is none, recommend cancellation or a written update.
### 2. Step 2

Cut attendees to deciders and the person with the facts.
### 3. Step 3

Require a one-page pre-read. No pre-read, no meeting.
### 4. Step 4

Exceptions only. Do not tour green metrics.
### 5. Step 5

End with owners and dates.
### 6. Step 6

Review the meeting itself after a few cycles and kill it if the decisions are still made in the hallway.

## Output

Deliver a **meeting system**.

- Purpose of this meeting system, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a meeting system by 30 September 2026. A weekly meeting has 18 people and has not made a decision in a month.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A weekly meeting has 18 people and has not made a decision in a month.

The meeting's supposed purpose: A weekly meeting has 18 people and has not made a decision in a month. Stated once, in the ask. Not written down anywhere else
Who attends: Diane Cho, operations manager
What decisions stall: A weekly meeting has 18 people and has not made a decision in a month
The pre-read if any: Tuesday shift, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Meeting system**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Cuts attendees, requires a pre-read, and cancels the meeting if no decision remains.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The meeting's supposed purpose | A weekly meeting has 18 people and has not made a decision in a month. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Who attends | Diane Cho, operations manager | Carried into the draft |
| What decisions stall | A weekly meeting has 18 people and has not made a decision in a month | Carried into the draft |
| The pre-read if any | Tuesday shift, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Write the decision the meeting exists to make. If there is none, recommend cancellation or a written update**

**2. Cut attendees to deciders and the person with the facts**

**3. Require a one-page pre-read. No pre-read, no meeting**

**4. Exceptions only. Do not tour green metrics**

**5. End with owners and dates**

**Deliberately not done**
- A status meeting with no decision.
- Inviting everyone.
- No pre-read.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A status meeting with no decision
- Inviting everyone
- No pre-read

## Related skills

- `operating-cadence`
- `status-report`
