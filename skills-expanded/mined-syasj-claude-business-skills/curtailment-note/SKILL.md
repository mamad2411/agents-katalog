---
name: curtailment-note
description: "Record a curtailment the user was instructed to make, with the volume and the time. Use when the user mentions curtailment, generation curtailment, instructed down, grid instruction, or asks for a curtailment note. Energy and utilities operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: energy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'curtailment-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Curtailment Note

Record a curtailment the user was instructed to make, with the volume and the time.

## When to use this skill

Use this skill when the user:

- curtailment
- generation curtailment
- instructed down
- grid instruction

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

- The instruction
- The volume
- The time
- The meter after

## Workflow


### 1. Step 1

Record the instruction as given.
### 2. Step 2

Record the volume they were told and the meter they have.
### 3. Step 3

Do not invent a compensation rate.
### 4. Step 4

Note if the meter does not show the drop.
### 5. Step 5

Name who acknowledges.
### 6. Step 6

This is not a dispute letter unless they ask for one.

## Output

Deliver a **curtailment note**.

- Purpose of this curtailment note, in two sentences.
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

The grid instruction was to drop 2 MW from 14:00 to 16:00 on 16 September. The meter shows a 1.4 MW drop. Compensation is not in the instruction.

### Example data

```text
instruction: drop 2 MW, 14:00-16:00, 16 Sep 2026
meter after: 1.4 MW below the prior hour
compensation rate: not in the instruction
who acknowledges: Devon Hale
```

### Example outcome

**Curtailment note**
Told: 2 MW, 14:00 to 16:00, 16 September.
Meter: 1.4 MW below the prior hour. Both figures stay. The gap is not edited away.
No compensation rate is in the instruction, so none is written.
This is a record, not a dispute letter.
Acknowledged by: Devon.

## Anti-patterns

- A compensation rate from memory
- A meter that does not match, ignored
- An instruction rewritten

## Related skills

- `demand-response-offer`
- `production-variance`
