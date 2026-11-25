---
name: feedback-on-work
description: "Give feedback on a learner's work that names the next improvement against the rubric. Use when the user mentions feedback on student work, coaching feedback, critique this assignment, formative feedback, or asks for a feedback note. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'feedback-on-work' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Feedback on Work

Give feedback on a learner's work that names the next improvement against the rubric.

## When to use this skill

Use this skill when the user:

- feedback on student work
- coaching feedback
- critique this assignment
- formative feedback

## When not to use this skill

- Completing graded work for submission

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

- The work
- The rubric or objective
- The learner's level
- What they may revise

## Workflow


### 1. Step 1

Start with what the work already achieves, specifically.
### 2. Step 2

Name the highest-leverage gap against the rubric.
### 3. Step 3

Show one concrete revision, not a rewrite of the whole piece for them to submit as their own.
### 4. Step 4

Limit comments. A margin full of nits hides the point.
### 5. Step 5

Invite a question.
### 6. Step 6

Do not complete a graded submission for the learner.

## Output

Deliver a **feedback note**.

- Purpose of this feedback note, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs a feedback note by 30 September 2026. A teacher wants the assistant to rewrite a student's essay so it will pass.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A teacher wants the assistant to rewrite a student's essay so it will pass.

The work: Module 2 lesson plan; Rubric draft. Both unassigned as of 14 September 2026
The rubric or objective: A teacher wants the assistant to rewrite a student's essay so it will pass. Stated once, in the ask. Not written down anywhere else
The learner's level: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
What they may revise: A teacher wants the assistant to rewrite a student's essay so it will pass
```

### Example outcome

**Feedback note**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Feedback that points to the rubric gap and shows a small example revision the student must still do themselves.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The work | Module 2 lesson plan; Rubric draft. Both unassigned as of 14 September 2026 | Needs confirmation |
| The rubric or objective | A teacher wants the assistant to rewrite a student's essay so it will pass. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| The learner's level | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| What they may revise | A teacher wants the assistant to rewrite a student's essay so it will pass | Needs confirmation |

**How this draft was built**

**1. Start with what the work already achieves, specifically**

**2. Name the highest-leverage gap against the rubric**

**3. Show one concrete revision, not a rewrite of the whole piece for them to submit as their own**

**4. Limit comments. A margin full of nits hides the point**

**5. Invite a question**

**Deliberately not done**
- Rewriting their graded work.
- Feedback with no next step.
- Comments unrelated to the rubric.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Rewriting their graded work
- Feedback with no next step
- Comments unrelated to the rubric

## Related skills

- `rubric-builder`
- `coaching-session`
