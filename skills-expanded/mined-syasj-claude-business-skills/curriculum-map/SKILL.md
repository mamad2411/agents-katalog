---
name: curriculum-map
description: "Map a curriculum so outcomes, courses, and assessments line up without gaps or pointless overlap. Use when the user mentions curriculum map, program map, course sequence, outcome alignment, or asks for a curriculum map. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'curriculum-map' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Curriculum Map

Map a curriculum so outcomes, courses, and assessments line up without gaps or pointless overlap.

## When to use this skill

Use this skill when the user:

- curriculum map
- program map
- course sequence
- outcome alignment

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

- Program outcomes
- Courses or modules
- Existing assessments
- Constraints

## Workflow


### 1. Step 1

List program outcomes the user confirmed. Do not invent accreditation standards.
### 2. Step 2

Show where each outcome is taught and assessed. An outcome with no assessment is a gap.
### 3. Step 3

Mark redundant assessments that do not add evidence.
### 4. Step 4

Sequence prerequisites they actually require.
### 5. Step 5

Note workload spikes.
### 6. Step 6

Flag external approval as a question if they said a regulator or institution must sign.

## Output

Deliver a **curriculum map**.

- Purpose of this curriculum map, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs a curriculum map by 30 September 2026. A program claims a communication outcome and no course assesses it.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A program claims a communication outcome and no course assesses it.

Program outcomes: A program claims a communication outcome and no course assesses it. Stated once, in the ask. Not written down anywhere else
Courses or modules: Rubric draft, last reviewed 14 September 2026. No owner named since
Existing assessments: Rubric draft, last reviewed 14 September 2026. No owner named since
Constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Curriculum map**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows the gap and recommends where an assessment should sit.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Program outcomes | A program claims a communication outcome and no course assesses it. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Courses or modules | Rubric draft, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Existing assessments | Rubric draft, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. List program outcomes the user confirmed. Do not invent accreditation standards**

**2. Show where each outcome is taught and assessed. An outcome with no assessment is a gap**

**3. Mark redundant assessments that do not add evidence**

**4. Sequence prerequisites they actually require**

**5. Note workload spikes**

**Deliberately not done**
- Invented accreditation clauses.
- An outcome never assessed.
- A map that hides workload spikes.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented accreditation clauses
- An outcome never assessed
- A map that hides workload spikes

## Related skills

- `syllabus-outline`
- `learning-objectives`
