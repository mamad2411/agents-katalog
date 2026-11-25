---
name: disruption-message
description: "Write the customer message for a cancellation with the rebooking fact they have. Use when the user mentions cancellation message, disruption text, flight cancelled note, rebooking message, or asks for a disruption note. Airline operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: airline
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'disruption-message' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Disruption Message

Write the customer message for a cancellation with the rebooking fact they have.

## When to use this skill

Use this skill when the user:

- cancellation message
- disruption text
- flight cancelled note
- rebooking message

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not advise exceeding a duty limit, skipping a maintenance release, or concealing a safety issue. Passenger messages must match the facts supplied.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The flight
- The rebooking they can offer
- Care they can offer
- What they cannot promise

## Workflow


### 1. Step 1

Say the flight is cancelled.
### 2. Step 2

Offer only the rebooking in the file.
### 3. Step 3

Say if no seat is confirmed.
### 4. Step 4

Care follows their rule.
### 5. Step 5

Do not promise a refund amount.
### 6. Step 6

Do not blame crew or maintenance unless they authorized that reason.

## Output

Deliver a **disruption note**.

- Purpose of this disruption note, in two sentences.
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

KA188 is cancelled. No replacement seat is confirmed. A draft promises the 10:00 departure and a full refund. The station may say they are still searching for a seat.

### Example data

```text
flight: KA188
status: cancelled
rebooking confirmed: none
care authorized: say they are searching for a seat
refund amount: not in the file
reason authorized: none
```

### Example outcome

**Message**
KA188 is cancelled. We do not have a confirmed seat yet. We are still searching.

**Not in the message**
The 10:00. A full refund. A cause. None of those are in the file.

## Anti-patterns

- A confirmed seat that is not confirmed
- A refund amount invented
- A cause they did not authorize

## Related skills

- `delay-message`
- `irrops-brief`
