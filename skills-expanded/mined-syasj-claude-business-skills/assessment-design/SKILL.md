---
name: assessment-design
description: "Design an assessment that matches the objective and resists cheating without becoming a trap. Use when the user mentions design an assessment, quiz design, test blueprint, check for understanding, or asks for a assessment. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'assessment-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Assessment Design

Design an assessment that matches the objective and resists cheating without becoming a trap.

## When to use this skill

Use this skill when the user:

- design an assessment
- quiz design
- test blueprint
- check for understanding

## When not to use this skill

- Completing graded work for a student
- Covert exam surveillance

## Professional boundary

Learning design supports the instructor. Do not complete graded work for a student or help anyone cheat. Do not invent accreditation requirements.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The objectives
- The format
- The time
- Integrity constraints they care about

## Workflow


### 1. Step 1

Map every item to an objective. Unmapped items are cut.
### 2. Step 2

Prefer a task that resembles the real performance when that is possible.
### 3. Step 3

Write a rubric or answer key from the objective, not from trick wording.
### 4. Step 4

Include a reasonable time box.
### 5. State the integrity rules they want

open notes or not. Do not design a surveillance product.
### 6. Step 6

This skill does not write answers for a student to submit as their own.

## Output

Deliver a **assessment**.

- Purpose of this assessment, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs an assessment by 30 September 2026. A manager wants an assessment that catches cheaters by using hidden webcams.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants an assessment that catches cheaters by using hidden webcams.

The objectives: A manager wants an assessment that catches cheaters by using hidden webcams. Stated once, in the ask. Not written down anywhere else
The format: plain, for people who already know the context. No house guide attached
The time: five working days, due 30 September 2026
Integrity constraints they care about: no extra headcount, and no result that is not in this file
```

### Example outcome

**Assessment**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Do not require covert cameras.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The objectives | A manager wants an assessment that catches cheaters by using hidden webcams. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The format | plain, for people who already know the context. No house guide attached | Carried into the draft |
| The time | five working days, due 30 September 2026 | Carried into the draft |
| Integrity constraints they care about | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Map every item to an objective. Unmapped items are cut**

**2. Prefer a task that resembles the real performance when that is possible**

**3. Write a rubric or answer key from the objective, not from trick wording**

**4. Include a reasonable time box**

**5. State the integrity rules they want**  
open notes or not. Do not design a surveillance product.

**Deliberately not done**
- Trick questions with no objective.
- A cheating service.
- Surveillance as the assessment.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Trick questions with no objective
- A cheating service
- Surveillance as the assessment

## Related skills

- `rubric-builder`
- `academic-integrity`
