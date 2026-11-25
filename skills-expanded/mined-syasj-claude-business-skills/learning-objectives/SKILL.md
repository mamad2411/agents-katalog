---
name: learning-objectives
description: "Write learning objectives that name the performance, the condition, and the standard. Use when the user mentions learning objectives, write objectives, course outcomes, training objectives, or asks for a learning objectives. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'learning-objectives' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Learning Objectives

Write learning objectives that name the performance, the condition, and the standard.

## When to use this skill

Use this skill when the user:

- learning objectives
- write objectives
- course outcomes
- training objectives

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- The performance needed on the job or in the course
- The conditions
- The standard they will accept
- The level of the learner

## Workflow


### 1. Step 1

Use a verb the learner can be seen doing.
### 2. Add the condition

with what notes, tools, or data.
### 3. Add the standard

how good is good enough, if the user knows it.
### 4. Step 4

Cut objectives the time budget cannot assess.
### 5. Step 5

Align each objective to a later practice or assessment.
### 6. Step 6

Do not write 'understand' as the only verb.

## Output

Deliver a **learning objectives**.

- Purpose of this learning objectives, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs a learning objectives by 30 September 2026. Objectives say 'understand compliance' for a one-hour briefing.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

Objectives say 'understand compliance' for a one-hour briefing.

The performance needed on the job or in the course: 75 in the last period. No prior period attached, so no trend
The conditions: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
The standard they will accept: their one-page rule dated 2 Mar 2026. No exception log since
The level of the learner: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Learning objectives**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Objectives that name a visible performance, such as spotting a missing control, and drop the vague verb.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The performance needed on the job or in the course | 75 in the last period. No prior period attached, so no trend | Needs confirmation |
| The conditions | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The standard they will accept | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| The level of the learner | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Use a verb the learner can be seen doing**

**2. Add the condition**  
with what notes, tools, or data.

**3. Add the standard**  
how good is good enough, if the user knows it.

**4. Cut objectives the time budget cannot assess**

**5. Align each objective to a later practice or assessment**

**Deliberately not done**
- Understand as the only verb.
- Objectives with no assessment path.
- A list longer than the course can teach.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Understand as the only verb
- Objectives with no assessment path
- A list longer than the course can teach

## Related skills

- `lesson-plan`
- `assessment-design`
