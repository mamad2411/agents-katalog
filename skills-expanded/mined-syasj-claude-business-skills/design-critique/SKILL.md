---
name: design-critique
description: "Critique a design against the user job and the constraints, with changes ranked. Use when the user mentions design critique, UX critique, review this design, critique the mock, or asks for a design critique. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'design-critique' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Design Critique

Critique a design against the user job and the constraints, with changes ranked.

## When to use this skill

Use this skill when the user:

- design critique
- UX critique
- review this design
- critique the mock

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Design critique improves the work. Do not copy a third party's branded assets. Accessibility is part of done, not a later pass to skip.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The user job
- The design or a description
- Constraints
- Known evidence

## Workflow


### 1. Step 1

Restate the job the screen must finish.
### 2. Step 2

Name what works, specifically, so the critique is usable.
### 3. Step 3

Rank issues by whether they block the job, not by taste.
### 4. Step 4

Recommend a change for each blocking issue.
### 5. Step 5

Separate evidence from taste.
### 6. Step 6

Do not redesign the brand for sport, and do not copy a third party's branded work.

## Output

Deliver a **design critique**.

- Purpose of this design critique, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs a design critique by 30 September 2026. A critique debates the font while the primary action is below the fold on the task's only screen.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A critique debates the font while the primary action is below the fold on the task's only screen.

The user job: Checkout screen v4, recorded 14 September 2026. No supporting file attached
The design or a description: Checkout screen v4, recorded 14 September 2026. No supporting file attached
Constraints: no extra headcount, and no result that is not in this file
Known evidence: one PDF, 2 pages, dated 14 September 2026
```

### Example outcome

**Design critique**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Leads with the blocked action and treats the font as secondary.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The user job | Checkout screen v4, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The design or a description | Checkout screen v4, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Constraints | no extra headcount, and no result that is not in this file | Carried into the draft |
| Known evidence | one PDF, 2 pages, dated 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Restate the job the screen must finish**

**2. Name what works, specifically, so the critique is usable**

**3. Rank issues by whether they block the job, not by taste**

**4. Recommend a change for each blocking issue**

**5. Separate evidence from taste**

**Deliberately not done**
- Taste comments with no job impact.
- A copy of a famous product.
- No ranked issues.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Taste comments with no job impact
- A copy of a famous product
- No ranked issues

## Related skills

- `usability-findings`
- `visual-hierarchy-review`
