---
name: instructional-design-brief
description: "Brief a designer or trainer on a learning experience with audience, objective, and constraints. Use when the user mentions instructional design brief, training brief, e-learning brief, course brief, or asks for a design brief for learning. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'instructional-design-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Instructional Design Brief

Brief a designer or trainer on a learning experience with audience, objective, and constraints.

## When to use this skill

Use this skill when the user:

- instructional design brief
- training brief
- e-learning brief
- course brief

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

- Audience
- Objective
- Time and format
- Assessment

## Workflow


### 1. Step 1

Describe the audience by what they already do.
### 2. Step 2

Write the objective as a performance.
### 3. Step 3

Choose a format that fits the objective. A video is not automatically better.
### 4. Step 4

Include practice and assessment in the brief, not as an afterthought.
### 5. Step 5

List source material they may use. Do not tell anyone to copy a third-party course.
### 6. Step 6

State review and update ownership.

## Output

Deliver a **design brief for learning**.

- Purpose of this design brief for learning, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs a design brief for learning by 30 September 2026. A brief asks for a fun video and has no objective.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A brief asks for a fun video and has no objective.

Audience: people who already buy from Riverbend College
Objective: A brief asks for a fun video and has no objective. Stated once, in the ask. Not written down anywhere else
Time and format: five working days, due 30 September 2026
Assessment: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Design brief for learning**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks production until the performance and the practice are written.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Audience | people who already buy from Riverbend College | Needs confirmation |
| Objective | A brief asks for a fun video and has no objective. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Time and format | five working days, due 30 September 2026 | Carried into the draft |
| Assessment | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Describe the audience by what they already do**

**2. Write the objective as a performance**

**3. Choose a format that fits the objective. A video is not automatically better**

**4. Include practice and assessment in the brief, not as an afterthought**

**5. List source material they may use. Do not tell anyone to copy a third-party course**

**Deliberately not done**
- A brief with no practice.
- Copying a proprietary course.
- Format chosen for fashion.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A brief with no practice
- Copying a proprietary course
- Format chosen for fashion

## Related skills

- `creative-brief`
- `lesson-plan`
