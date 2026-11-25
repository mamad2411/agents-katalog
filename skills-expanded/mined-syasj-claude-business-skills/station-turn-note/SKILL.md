---
name: station-turn-note
description: "Record a turn delay with the minute it started and the cause the ramp lead wrote. Use when the user mentions turnaround delay, aircraft turn, gate delay, ramp delay, or asks for a turn note. Airline operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: airline
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'station-turn-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Station Turn Note

Record a turn delay with the minute it started and the cause the ramp lead wrote.

## When to use this skill

Use this skill when the user:

- turnaround delay
- aircraft turn
- gate delay
- ramp delay

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
- The scheduled turn
- The actual
- The cause they wrote

## Workflow


### 1. Step 1

Show scheduled and actual.
### 2. Step 2

Use their cause words.
### 3. Step 3

Do not add a department to blame.
### 4. Step 4

Note if the next flight is the same aircraft.
### 5. Step 5

Name who updates control.
### 6. Step 6

Do not hide a minute to protect a target.

## Output

Deliver a **turn note**.

- Purpose of this turn note, in two sentences.
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

KA412's turn was scheduled at 40 minutes and took 55. The ramp note says the bag cart was late. A draft blames cabin cleaning so the ramp target holds.

### Example data

```text
flight: KA412
scheduled turn: 40 minutes
actual: 55
ramp note: late bag cart
draft cause: cabin cleaning
same aircraft next: KA188
who updates control: Luis Ortega
```

### Example outcome

**Turn note**
55 against 40. Fifteen minutes. Cause in the ramp note: late bag cart.
Cabin cleaning is not in the note. It does not replace the cart.
Next flight on the same aircraft: KA188. Control needs the 15 minutes, not a cleaned-up cause.
Updater: Luis.

## Anti-patterns

- A cause rewritten to protect a target
- Missing minutes
- Blame with no note

## Related skills

- `irrops-brief`
- `route-result-note`
