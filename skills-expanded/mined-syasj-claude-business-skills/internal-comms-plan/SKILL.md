---
name: internal-comms-plan
description: "Plan an internal message for a change people must understand, with the hard part said plainly. Use when the user mentions internal comms, announce a change, staff communication, leadership message, or asks for a internal comms plan. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'internal-comms-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Internal Communications Plan

Plan an internal message for a change people must understand, with the hard part said plainly.

## When to use this skill

Use this skill when the user:

- internal comms
- announce a change
- staff communication
- leadership message

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

- The change
- The audience
- What they will lose or must do
- The speaker

## Workflow


### 1. Step 1

State the change in one sentence a frontline person can repeat.
### 2. Step 2

Include what it means for their Tuesday.
### 3. Say the hard part if the user has confirmed it

timing, workload, or role impact. Do not hide a layoff or a pay change in soft language, and do not help deceive staff.
### 4. Step 4

Choose the speaker who can answer questions.
### 5. Step 5

Provide a question path.
### 6. Step 6

Follow with a short FAQ grounded in decisions already made, not in hopes.

## Output

Deliver a **internal comms plan**.

- Purpose of this internal comms plan, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs an internal comms plan by 30 September 2026. A memo announces 'exciting operating model evolution' and never says whose work changes.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A memo announces 'exciting operating model evolution' and never says whose work changes.

The change: requested 14 September 2026. Not yet approved
The audience: people who already buy from Harbor Goods
What they will lose or must do: A memo announces 'exciting operating model evolution' and never says whose work changes
The speaker: Tuesday shift, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Internal comms plan**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Says whose work changes, who will answer questions, and what stays the same.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The change | requested 14 September 2026. Not yet approved | Needs confirmation |
| The audience | people who already buy from Harbor Goods | Carried into the draft |
| What they will lose or must do | A memo announces 'exciting operating model evolution' and never says whose work changes | Carried into the draft |
| The speaker | Tuesday shift, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. State the change in one sentence a frontline person can repeat**

**2. Include what it means for their Tuesday**

**3. Say the hard part if the user has confirmed it**  
timing, workload, or role impact. Do not hide a layoff or a pay change in soft language, and do not help deceive staff.

**4. Choose the speaker who can answer questions**

**5. Provide a question path**

**Deliberately not done**
- A message that hides a confirmed hard impact.
- No question path.
- Jargon in the first line.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A message that hides a confirmed hard impact
- No question path
- Jargon in the first line

## Related skills

- `change-leadership`
- `stakeholder-map`
