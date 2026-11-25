---
name: lesson-plan
description: "Plan a lesson from an objective, a practice task, and a check for understanding. Use when the user mentions lesson plan, plan a class, teaching plan, session plan, or asks for a lesson plan. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'lesson-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Lesson Plan

Plan a lesson from an objective, a practice task, and a check for understanding.

## When to use this skill

Use this skill when the user:

- lesson plan
- plan a class
- teaching plan
- session plan

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

- The learners
- The objective
- Time available
- Materials they have

## Workflow


### 1. Step 1

Write an objective learners can demonstrate, not a topic label.
### 2. Step 2

Open with a reason the objective matters to their work or course.
### 3. Step 3

Teach one model, then a practice task. A lecture with no practice is a finding.
### 4. Step 4

Check understanding before the end.
### 5. Step 5

Plan the likely misconception they named, or mark it unknown.
### 6. Step 6

Fit the plan to the minutes. Cut content before cutting the check.

## Output

Deliver a **lesson plan**.

- Purpose of this lesson plan, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs a lesson plan by 30 September 2026. A 40-minute plan has 30 slides and no task.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A 40-minute plan has 30 slides and no task.

The learners: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
The objective: A 40-minute plan has 30 slides and no task. Stated once, in the ask. Not written down anywhere else
Time available: five working days, due 30 September 2026
Materials they have: Rubric draft, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Lesson plan**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A plan with one objective, one practice task, and a check, with slides cut to fit.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The learners | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The objective | A 40-minute plan has 30 slides and no task. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Time available | five working days, due 30 September 2026 | Carried into the draft |
| Materials they have | Rubric draft, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Write an objective learners can demonstrate, not a topic label**

**2. Open with a reason the objective matters to their work or course**

**3. Teach one model, then a practice task. A lecture with no practice is a finding**

**4. Check understanding before the end**

**5. Plan the likely misconception they named, or mark it unknown**

**Deliberately not done**
- An objective that is only a topic.
- No practice.
- A plan that overruns and skips the check.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An objective that is only a topic
- No practice
- A plan that overruns and skips the check

## Related skills

- `learning-objectives`
- `assessment-design`
