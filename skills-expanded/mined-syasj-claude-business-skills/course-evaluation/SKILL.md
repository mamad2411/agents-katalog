---
name: course-evaluation
description: "Read a course evaluation without overreacting to a small sample or a single cruel comment. Use when the user mentions course evaluation, training feedback, class survey, workshop feedback, or asks for a evaluation readout. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'course-evaluation' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Course Evaluation Readout

Read a course evaluation without overreacting to a small sample or a single cruel comment.

## When to use this skill

Use this skill when the user:

- course evaluation
- training feedback
- class survey
- workshop feedback

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

- The results
- Response rate
- The objectives
- Comments they pasted

## Workflow


### 1. Step 1

Report response rate before scores.
### 2. Step 2

Tie low scores to a specific objective or logistics issue if the comments support it.
### 3. Step 3

Do not let one abusive comment rewrite the course. Quote only what is useful and safe.
### 4. Step 4

Recommend one change before the next run.
### 5. Step 5

Protect respondent identity in small groups.
### 6. Step 6

Ignore requests to punish a teacher from anonymous venting with no process.

## Output

Deliver a **evaluation readout**.

- Purpose of this evaluation readout, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs an evaluation readout by 30 September 2026. A leader wants to remove a trainer because one unnamed comment was harsh and the response rate was low.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A leader wants to remove a trainer because one unnamed comment was harsh and the response rate was low.

The results: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
Response rate: 30 in the last period. No prior period attached, so no trend
The objectives: A leader wants to remove a trainer because one unnamed comment was harsh and the response rate was low. Stated once, in the ask. Not written down anywhere else
Comments they pasted: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Evaluation readout**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the removal, states the sample limit, and proposes one evidence-based change.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The results | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Response rate | 30 in the last period. No prior period attached, so no trend | Carried into the draft |
| The objectives | A leader wants to remove a trainer because one unnamed comment was harsh and the response rate was low. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Comments they pasted | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Report response rate before scores**

**2. Tie low scores to a specific objective or logistics issue if the comments support it**

**3. Do not let one abusive comment rewrite the course. Quote only what is useful and safe**

**4. Recommend one change before the next run**

**5. Protect respondent identity in small groups**

**Deliberately not done**
- A redesign from three responses.
- Identifying a respondent.
- Punishment from an anonymous vent.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A redesign from three responses
- Identifying a respondent
- Punishment from an anonymous vent

## Related skills

- `survey-analysis`
- `lesson-plan`
