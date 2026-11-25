---
name: baggage-irregularity
description: "Record a bag irregularity with the tag, the flight, and the status they know. Use when the user mentions baggage claim, delayed bag, bag irregularity, lost bag file, or asks for a bag note. Airline operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: airline
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'baggage-irregularity' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Baggage Irregularity

Record a bag irregularity with the tag, the flight, and the status they know.

## When to use this skill

Use this skill when the user:

- baggage claim
- delayed bag
- bag irregularity
- lost bag file

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

- The tag
- The flight
- The status
- What the passenger was told

## Workflow


### 1. Step 1

Record the tag and the flight.
### 2. Use the status they know

delayed, not lost, unless they said lost.
### 3. Step 3

Do not promise a delivery hour they do not have.
### 4. Step 4

Match the passenger message to the status.
### 5. Step 5

Name the owner of the file.
### 6. Step 6

Do not ask for a passport number in the note.

## Output

Deliver a **bag note**.

- Purpose of this bag note, in two sentences.
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

Tag 8812 did not arrive on KA412. Status in the system is delayed. A text already told the passenger the bag would be at the house by 8 p.m. Nobody has a delivery time.

### Example data

```text
tag: 8812
flight: KA412
status: delayed
passenger told: at the house by 20:00
delivery time on file: none
owner: station baggage desk
passport number: do not collect
```

### Example outcome

**Bag file — 8812**
Status: delayed, off KA412. Do not write lost.
The 20:00 house delivery was not known. Send a correction: we do not have a delivery time.
Owner: the baggage desk.
Do not put a passport number in this file.

## Anti-patterns

- Lost written when the status is delayed
- A delivery hour invented
- Identity documents in the note

## Related skills

- `delay-message`
- `customer-communication-incident`
