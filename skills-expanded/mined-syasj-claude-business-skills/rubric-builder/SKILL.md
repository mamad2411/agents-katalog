---
name: rubric-builder
description: "Build a rubric with levels a second marker could apply to the same work. Use when the user mentions rubric, marking guide, scoring guide, assessment criteria, or asks for a rubric. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'rubric-builder' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Rubric Builder

Build a rubric with levels a second marker could apply to the same work.

## When to use this skill

Use this skill when the user:

- rubric
- marking guide
- scoring guide
- assessment criteria

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

- The task
- The qualities that matter
- The scale they use
- Examples of strong and weak work if any

## Workflow


### 1. Step 1

Criteria come from the objective, not from personal taste.
### 2. Step 2

Describe each level with observable features.
### 3. Step 3

Weight criteria they say matter more. If they have no weights, keep them equal and say so.
### 4. Step 4

Add one example descriptor only from work they supplied.
### 5. Step 5

Test the rubric against two samples if they have them.
### 6. Step 6

Cut criteria that reward polish unrelated to the objective unless they intend that.

## Output

Deliver a **rubric**.

- Purpose of this rubric, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs a rubric by 30 September 2026. A rubric says 'excellent analysis' with no description of what excellent contains.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A rubric says 'excellent analysis' with no description of what excellent contains.

The task: A rubric says 'excellent analysis' with no description of what excellent contains. Stated once, in the ask. Not written down anywhere else
The qualities that matter: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
The scale they use: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
Examples of strong and weak work if any: Module 2 lesson plan; Rubric draft. Both unassigned as of 14 September 2026
```

### Example outcome

**Rubric**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A rubric whose top level names the comparisons or evidence a marker must see.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The task | A rubric says 'excellent analysis' with no description of what excellent contains. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The qualities that matter | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The scale they use | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Examples of strong and weak work if any | Module 2 lesson plan; Rubric draft. Both unassigned as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Criteria come from the objective, not from personal taste**

**2. Describe each level with observable features**

**3. Weight criteria they say matter more. If they have no weights, keep them equal and say so**

**4. Add one example descriptor only from work they supplied**

**5. Test the rubric against two samples if they have them**

**Deliberately not done**
- Vague levels such as good and excellent with no features.
- Hidden criteria.
- A rubric that rewards length only.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Vague levels such as good and excellent with no features
- Hidden criteria
- A rubric that rewards length only

## Related skills

- `assessment-design`
- `feedback-on-work`
