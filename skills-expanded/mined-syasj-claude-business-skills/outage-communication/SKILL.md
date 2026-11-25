---
name: outage-communication
description: "Draft an outage message with the area, the known cause label, and the next update time. Use when the user mentions outage message, power outage update, utility customer message, restoration update, or asks for a outage message. Energy and utilities operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: energy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'outage-communication' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Outage Communication

Draft an outage message with the area, the known cause label, and the next update time.

## When to use this skill

Use this skill when the user:

- outage message
- power outage update
- utility customer message
- restoration update

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational energy advice is not a permit and not a safety case. Do not bypass lockout, isolation, or regulatory limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The affected area
- What is confirmed
- The next update time
- The approver

## Workflow


### 1. Step 1

State who is affected in the terms they confirmed.
### 2. Step 2

Do not guess a cause.
### 3. Step 3

Give the next update time.
### 4. Step 4

Include safety instructions they already approved, such as staying away from downed lines. Do not invent technical bypass steps.
### 5. Step 5

Avoid promising a restoration minute they do not have.
### 6. Step 6

Keep the log of what was said.

## Output

Deliver a **outage message**.

- Purpose of this outage message, in two sentences.
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

Devon Hale, operations superintendent at Prairie Line Energy in Grande Prairie, needs an outage message by 30 September 2026. A message promises power in 30 minutes because that sounded reassuring.

### Example data

```text
From: Devon Hale, operations superintendent
Organization: Prairie Line Energy, Grande Prairie
Date: 14 September 2026
Needed by: 30 September 2026

A message promises power in 30 minutes because that sounded reassuring.

The affected area: Feeder 12, recorded 14 September 2026. No supporting file attached
What is confirmed: September bill, last reviewed 14 September 2026. No owner named since
The next update time: five working days, due 30 September 2026
The approver: Devon Hale. They have not signed
```

### Example outcome

**Outage message**
To: Devon Hale, operations superintendent, Prairie Line Energy
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the 30-minute promise and commits to a next update.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The affected area | Feeder 12, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| What is confirmed | September bill, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The next update time | five working days, due 30 September 2026 | Carried into the draft |
| The approver | Devon Hale. They have not signed | Needs confirmation |

**How this draft was built**

**1. State who is affected in the terms they confirmed**

**2. Do not guess a cause**

**3. Give the next update time**

**4. Include safety instructions they already approved, such as staying away from downed lines. Do not invent technical bypass steps**

**5. Avoid promising a restoration minute they do not have**

**Deliberately not done**
- A guessed cause.
- A fake restoration minute.
- Bypass instructions for equipment.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Devon Hale by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A guessed cause
- A fake restoration minute
- Bypass instructions for equipment

## Related skills

- `customer-communication-incident`
- `service-recovery`
