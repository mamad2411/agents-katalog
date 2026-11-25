---
name: training-needs-analysis
description: "Decide whether a performance gap is a training problem or a job-design problem. Use when the user mentions training needs, skills gap, do they need training, needs analysis, or asks for a training needs note. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'training-needs-analysis' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Training Needs Analysis

Decide whether a performance gap is a training problem or a job-design problem.

## When to use this skill

Use this skill when the user:

- training needs
- skills gap
- do they need training
- needs analysis

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

- The performance gap
- Evidence
- What training already exists
- Constraints on the job

## Workflow


### 1. Step 1

Describe the gap as observable work.
### 2. Step 2

Ask whether people could do the task with enough time and tools. If not, training is the wrong first fix.
### 3. Step 3

If the skill is missing, define the smallest training that builds it.
### 4. Step 4

Name who needs it and who does not, so you do not train the whole company by habit.
### 5. Step 5

State how you will know the gap closed.
### 6. Step 6

Recommend a job-design fix when the evidence points there.

## Output

Deliver a **training needs note**.

- Purpose of this training needs note, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs a training needs note by 30 September 2026. Errors rose after a tool change that hides the needed field, and the draft recommends a full-day course.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

Errors rose after a tool change that hides the needed field, and the draft recommends a full-day course.

The performance gap: Module 2 lesson plan is missing a source
Evidence: one PDF, 2 pages, dated 14 September 2026
What training already exists: Thursday workshop, last reviewed 14 September 2026. No owner named since
Constraints on the job: no extra headcount, and no result that is not in this file
```

### Example outcome

**Training needs note**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Fixes the field first and limits training to the people who still lack the skill.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The performance gap | Module 2 lesson plan is missing a source | Needs confirmation |
| Evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| What training already exists | Thursday workshop, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Constraints on the job | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Describe the gap as observable work**

**2. Ask whether people could do the task with enough time and tools. If not, training is the wrong first fix**

**3. If the skill is missing, define the smallest training that builds it**

**4. Name who needs it and who does not, so you do not train the whole company by habit**

**5. State how you will know the gap closed**

**Deliberately not done**
- Training as the answer to a tooling or workload problem.
- A course with no success check.
- Training everyone by default.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Training as the answer to a tooling or workload problem
- A course with no success check
- Training everyone by default

## Related skills

- `learning-path`
- `lesson-plan`
