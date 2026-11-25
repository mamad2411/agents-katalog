---
name: program-logic
description: "Draft a program logic model that shows inputs, activities, and outcomes without pretending impact is proven. Use when the user mentions logic model, theory of change, program logic, outcome model, or asks for a logic model. Nonprofit and public interest skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: nonprofit
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'program-logic' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Program Logic

Draft a program logic model that shows inputs, activities, and outcomes without pretending impact is proven.

## When to use this skill

Use this skill when the user:

- logic model
- theory of change
- program logic
- outcome model

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent impact metrics or donor intent. Fundraising copy must be accurate and free of pressure tactics that misstate the need.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Inputs they have
- Activities
- Intended outcomes
- Evidence so far

## Workflow


### 1. Step 1

Start from activities they actually run.
### 2. Step 2

Write outcomes as changes, and label them intended if unmeasured.
### 3. Step 3

Show the assumption between activity and outcome.
### 4. Step 4

Do not draw an impact arrow they have not tested.
### 5. Step 5

Note missing data.
### 6. Step 6

Keep the model to one program.

## Output

Deliver a **logic model**.

- Purpose of this logic model, in two sentences.
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

Amira Hassan, program director at Open Kitchen Society in Calgary, needs a logic model by 30 September 2026. A logic model says the workshop causes employment, and nobody tracked jobs.

### Example data

```text
From: Amira Hassan, program director
Organization: Open Kitchen Society, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A logic model says the workshop causes employment, and nobody tracked jobs.

Inputs they have: Grant report draft and one other, both unconfirmed as of 14 September 2026
Activities: Grant report draft. Stated in the ask, not documented anywhere else
Intended outcomes: A logic model says the workshop causes employment, and nobody tracked jobs. Stated once, in the ask. Not written down anywhere else
Evidence so far: one PDF, 2 pages, dated 14 September 2026
```

### Example outcome

**Logic model**
To: Amira Hassan, program director, Open Kitchen Society
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Labels employment as intended and names the missing measure.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Inputs they have | Grant report draft and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |
| Activities | Grant report draft. Stated in the ask, not documented anywhere else | Carried into the draft |
| Intended outcomes | A logic model says the workshop causes employment, and nobody tracked jobs. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Evidence so far | one PDF, 2 pages, dated 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Start from activities they actually run**

**2. Write outcomes as changes, and label them intended if unmeasured**

**3. Show the assumption between activity and outcome**

**4. Do not draw an impact arrow they have not tested**

**5. Note missing data**

**Deliberately not done**
- A proven-impact claim with no measure.
- Activities that are not real.
- A model of five programs at once.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Amira Hassan by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A proven-impact claim with no measure
- Activities that are not real
- A model of five programs at once

## Related skills

- `nonprofit-case-statement`
- `metric-definition`
