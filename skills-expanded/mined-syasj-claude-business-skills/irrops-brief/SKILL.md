---
name: irrops-brief
description: "Brief the station on a disrupted flight using the facts the controller has. Use when the user mentions irregular operations, IRROPS, disrupted flight, station brief, or asks for a ops brief. Airline operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: airline
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'irrops-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Irregular Ops Brief

Brief the station on a disrupted flight using the facts the controller has.

## When to use this skill

Use this skill when the user:

- irregular operations
- IRROPS
- disrupted flight
- station brief

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
- The reason they can state
- Passengers booked
- What is not known

## Workflow


### 1. Step 1

State the flight and the time.
### 2. Step 2

Use only the reason they have.
### 3. Step 3

Count passengers from their figure.
### 4. Step 4

Say what the station can do today.
### 5. Step 5

Do not invent a crew or a spare aircraft.
### 6. Step 6

Name the next update time.

## Output

Deliver a **ops brief**.

- Purpose of this ops brief, in two sentences.
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

KA412 YYZ-YYC is late. The controller's note says a ground hold. A draft brief blames maintenance. Booked passengers are 142. No spare aircraft is assigned.

### Example data

```text
flight: KA412 YYZ-YYC
fact: ground hold, note timed 16 Sep 2026 14:05
passengers booked: 142
spare aircraft: none assigned
next update promised: 15:00
station: YYC, Luis Ortega
```

### Example outcome

**Station brief — KA412**
Ground hold. That is the reason in the note. Maintenance comes out of the draft.
Passengers booked: 142.
No spare is assigned. Do not tell the station one is coming.
Next update: 15:00. Luis owns the board until then.

## Anti-patterns

- A cause they do not have
- A spare aircraft that is not assigned
- A passenger count from memory

## Related skills

- `delay-message`
- `station-turn-note`
