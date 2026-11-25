---
name: capa-plan
description: "Plan a corrective action that fixes a cause and checks that the fix worked. Use when the user mentions CAPA, corrective action, preventive action, quality action plan, or asks for a CAPA plan. Manufacturing and quality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: manufacturing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'capa-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# CAPA Plan

Plan a corrective action that fixes a cause and checks that the fix worked.

## When to use this skill

Use this skill when the user:

- CAPA
- corrective action
- preventive action
- quality action plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Quality and safety procedures are drafts for the site's quality system. Do not bypass a hold, calibration, or safety step.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The problem statement
- Evidence
- Suspected cause
- How effectiveness will be checked

## Workflow


### 1. Step 1

Write a problem statement with the defect and the impact.
### 2. Step 2

Separate containment already done from corrective action.
### 3. Step 3

Test the suspected cause against evidence. Do not jump to training as the cause by habit.
### 4. Step 4

Define the action, the owner, and the date.
### 5. Step 5

Define the effectiveness check and when it happens.
### 6. Step 6

Close only when the check passes. Training attendance is not effectiveness by itself.

## Output

Deliver a **CAPA plan**.

- Purpose of this CAPA plan, in two sentences.
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

Gus Moretti, plant manager at Redline Parts in Nisku, needs a CAPA plan by 30 September 2026. A CAPA closes because operators signed a training sheet, and the defect is still appearing.

### Example data

```text
From: Gus Moretti, plant manager
Organization: Redline Parts, Nisku
Date: 14 September 2026
Needed by: 30 September 2026

A CAPA closes because operators signed a training sheet, and the defect is still appearing.

The problem statement: A CAPA closes because operators signed a training sheet, and the defect is still appearing. Stated once, in the ask. Not written down anywhere else
Evidence: one PDF, 2 pages, dated 14 September 2026
Suspected cause: Lot 26-0914 and one other, both unconfirmed as of 14 September 2026
How effectiveness will be checked: Lot 26-0914, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Capa plan**
To: Gus Moretti, plant manager, Redline Parts
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps the CAPA open until the defect measure moves, and looks past the training reflex.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The problem statement | A CAPA closes because operators signed a training sheet, and the defect is still appearing. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Suspected cause | Lot 26-0914 and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| How effectiveness will be checked | Lot 26-0914, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Write a problem statement with the defect and the impact**

**2. Separate containment already done from corrective action**

**3. Test the suspected cause against evidence. Do not jump to training as the cause by habit**

**4. Define the action, the owner, and the date**

**5. Define the effectiveness check and when it happens**

**Deliberately not done**
- Training as the default cause.
- Closure without an effectiveness check.
- A problem statement with no defect.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Gus Moretti by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Training as the default cause
- Closure without an effectiveness check
- A problem statement with no defect

## Related skills

- `nonconformance-report`
- `continuous-improvement`
