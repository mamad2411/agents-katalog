---
name: work-instruction
description: "Write a work instruction a new operator can follow, including the stop and the quality check. Use when the user mentions work instruction, standard work, operator instruction, job instruction, or asks for a work instruction. Manufacturing and quality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: manufacturing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'work-instruction' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Work Instruction

Write a work instruction a new operator can follow, including the stop and the quality check.

## When to use this skill

Use this skill when the user:

- work instruction
- standard work
- operator instruction
- job instruction

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Quality and safety procedures are drafts for the site's quality system. Do not bypass a hold, calibration, or safety step.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The outcome
- The steps as performed safely
- The check
- The stop conditions

## Workflow


### 1. Step 1

Start with the outcome and the safety precondition they require.
### 2. Step 2

Number steps in the order the work is done.
### 3. Step 3

Include the quality check and what a fail looks like.
### 4. Write the stop

when to call a lead.
### 5. Step 5

Use their terms for tools and parts. Do not rename equipment.
### 6. Step 6

Photos only if they supply them. Do not invent a torque or a setting.

## Output

Deliver a **work instruction**.

- Purpose of this work instruction, in two sentences.
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

Gus Moretti, plant manager at Redline Parts in Nisku, needs a work instruction by 30 September 2026. An instruction says 'tighten properly' and the torque is unknown.

### Example data

```text
From: Gus Moretti, plant manager
Organization: Redline Parts, Nisku
Date: 14 September 2026
Needed by: 30 September 2026

An instruction says 'tighten properly' and the torque is unknown.

The outcome: An instruction says 'tighten properly' and the torque is unknown. Stated once, in the ask. Not written down anywhere else
The steps as performed safely: Line 2; Lot 26-0914. Both unassigned as of 14 September 2026
The check: Line 2, recorded 14 September 2026. No supporting file attached
The stop conditions: Line 2, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Work instruction**
To: Gus Moretti, plant manager, Redline Parts
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Marks torque as a required input from engineering rather than inventing a number.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcome | An instruction says 'tighten properly' and the torque is unknown. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The steps as performed safely | Line 2; Lot 26-0914. Both unassigned as of 14 September 2026 | Carried into the draft |
| The check | Line 2, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The stop conditions | Line 2, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Start with the outcome and the safety precondition they require**

**2. Number steps in the order the work is done**

**3. Include the quality check and what a fail looks like**

**4. Write the stop**  
when to call a lead.

**5. Use their terms for tools and parts. Do not rename equipment**

**Deliberately not done**
- An invented setting.
- No stop condition.
- A step order that does not match the work.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Gus Moretti by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An invented setting
- No stop condition
- A step order that does not match the work

## Related skills

- `sop-writer`
- `quality-control-plan`
