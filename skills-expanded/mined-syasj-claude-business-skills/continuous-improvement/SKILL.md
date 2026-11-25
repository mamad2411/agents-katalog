---
name: continuous-improvement
description: "Frame an improvement from a measured problem, a small countermeasure, and a check. Use when the user mentions continuous improvement, kaizen, process improvement, fix this recurring issue, or asks for a improvement brief. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'continuous-improvement' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Continuous Improvement

Frame an improvement from a measured problem, a small countermeasure, and a check.

## When to use this skill

Use this skill when the user:

- continuous improvement
- kaizen
- process improvement
- fix this recurring issue

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The recurring problem
- The measure
- The suspected cause
- The time box

## Workflow


### 1. Step 1

State the problem as a gap in a measure they have.
### 2. Step 2

Go see the work before proposing a tool. Ask for the observation if they have not made one.
### 3. Step 3

Pick one suspected cause to test. A fishbone with no test is a poster.
### 4. Step 4

Propose a small countermeasure the team can run in the time box.
### 5. Step 5

Define the check that says it worked.
### 6. Step 6

Plan how the new way becomes the standard if the check passes.

## Output

Deliver a **improvement brief**.

- Purpose of this improvement brief, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs an improvement brief by 30 September 2026. A team wants new software because a weekly report is late, and nobody has watched the report being built.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A team wants new software because a weekly report is late, and nobody has watched the report being built.

The recurring problem: A team wants new software because a weekly report is late, and nobody has watched the report being built. Stated once, in the ask. Not written down anywhere else
The measure: Tuesday shift, recorded 14 September 2026. No supporting file attached
The suspected cause: Tuesday shift, recorded 14 September 2026. No supporting file attached
The time box: five working days, due 30 September 2026
```

### Example outcome

**Improvement brief**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Requires an observation of the current report path before any purchase.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The recurring problem | A team wants new software because a weekly report is late, and nobody has watched the report being built. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The measure | Tuesday shift, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The suspected cause | Tuesday shift, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The time box | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. State the problem as a gap in a measure they have**

**2. Go see the work before proposing a tool. Ask for the observation if they have not made one**

**3. Pick one suspected cause to test. A fishbone with no test is a poster**

**4. Propose a small countermeasure the team can run in the time box**

**5. Define the check that says it worked**

**Deliberately not done**
- A tool purchase as the first countermeasure.
- No measure.
- A brainstorm with no test.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A tool purchase as the first countermeasure
- No measure
- A brainstorm with no test

## Related skills

- `process-map`
- `capa-plan`
