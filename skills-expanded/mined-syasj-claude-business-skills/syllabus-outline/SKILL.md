---
name: syllabus-outline
description: "Outline a syllabus with outcomes, assessments, and policies the instructor actually uses. Use when the user mentions syllabus, course outline, module outline, class policies, or asks for a syllabus outline. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'syllabus-outline' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Syllabus Outline

Outline a syllabus with outcomes, assessments, and policies the instructor actually uses.

## When to use this skill

Use this skill when the user:

- syllabus
- course outline
- module outline
- class policies

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

- Outcomes
- Assessment list
- Schedule constraints
- Policies they want included

## Workflow


### 1. Step 1

Lead with outcomes and how students will be assessed.
### 2. Step 2

Map weeks or modules to outcomes. A week with no outcome is a candidate to cut.
### 3. Step 3

Include late, integrity, and support policies only as the instructor stated them. Do not invent an institutional rule.
### 4. Step 4

Show the workload honestly.
### 5. Step 5

Mark required materials they confirmed.
### 6. Step 6

Note what the institution must still approve if they said approval is required.

## Output

Deliver a **syllabus outline**.

- Purpose of this syllabus outline, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs a syllabus outline by 30 September 2026. A syllabus lists readings for fifteen weeks and one grade at the end.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A syllabus lists readings for fifteen weeks and one grade at the end.

Outcomes: A syllabus lists readings for fifteen weeks and one grade at the end. Stated once, in the ask. Not written down anywhere else
Assessment list: Module 2 lesson plan; Rubric draft; Thursday workshop
Schedule constraints: no extra headcount, and no result that is not in this file
Policies they want included: Thursday workshop, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Syllabus outline**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Maps assessments to outcomes and refuses to invent a university policy.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Outcomes | A syllabus lists readings for fifteen weeks and one grade at the end. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Assessment list | Module 2 lesson plan; Rubric draft; Thursday workshop | Carried into the draft |
| Schedule constraints | no extra headcount, and no result that is not in this file | Carried into the draft |
| Policies they want included | Thursday workshop, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Lead with outcomes and how students will be assessed**

**2. Map weeks or modules to outcomes. A week with no outcome is a candidate to cut**

**3. Include late, integrity, and support policies only as the instructor stated them. Do not invent an institutional rule**

**4. Show the workload honestly**

**5. Mark required materials they confirmed**

**Deliberately not done**
- Invented institutional rules.
- A week-by-week with no assessment map.
- Hidden workload.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented institutional rules
- A week-by-week with no assessment map
- Hidden workload

## Related skills

- `curriculum-map`
- `learning-objectives`
