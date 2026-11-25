---
name: delay-message
description: "Write the passenger message from the delay facts the station can say. Use when the user mentions delay message, passenger announcement, flight delay text, gate announcement, or asks for a passenger message. Airline operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: airline
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'delay-message' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Delay Message

Write the passenger message from the delay facts the station can say.

## When to use this skill

Use this skill when the user:

- delay message
- passenger announcement
- flight delay text
- gate announcement

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
- The new time if they have one
- The reason they may say
- Care they are allowed to offer

## Workflow


### 1. Step 1

Lead with the flight and the time.
### 2. Step 2

If the new time is unknown, say unknown.
### 3. Step 3

Use only the reason they authorized.
### 4. Step 4

Offer only the care they listed.
### 5. Step 5

Do not promise a connection.
### 6. Step 6

Do not blame a person.

## Output

Deliver a **passenger message**.

- Purpose of this passenger message, in two sentences.
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

Gate staff want a message for KA412. There is no new departure time. A draft says 18:40 and a free hotel. The station may offer water. It may not offer a hotel.

### Example data

```text
flight: KA412
new time: unknown
reason authorized: ground hold
care authorized: water at the gate
care not authorized: hotel, meal voucher
connections: not confirmed
```

### Example outcome

**Gate message**
KA412 is delayed for a ground hold. We do not have a new departure time.

Water is available at the gate. We cannot confirm a connection on this message.

**Not in the message**
18:40. A hotel. A meal voucher. A person to blame.

## Anti-patterns

- A fake new time
- A hotel they cannot offer
- A connection promise

## Related skills

- `irrops-brief`
- `disruption-message`
