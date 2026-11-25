---
name: nonprofit-case-statement
description: "Write a case for support from real need, real program facts, and a specific ask. Use when the user mentions case for support, fundraising narrative, case statement, donor narrative, or asks for a case statement. Nonprofit and public interest skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: nonprofit
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'nonprofit-case-statement' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Case Statement

Write a case for support from real need, real program facts, and a specific ask.

## When to use this skill

Use this skill when the user:

- case for support
- fundraising narrative
- case statement
- donor narrative

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

- The need they can evidence
- The program
- The ask
- What donors must not be told

## Workflow


### 1. Step 1

Describe the need with evidence they have.
### 2. Step 2

Explain what the program actually does.
### 3. Step 3

Separate outputs from outcomes.
### 4. Step 4

Make one ask.
### 5. Step 5

Do not invent a beneficiary story or a success rate.
### 6. Step 6

Avoid pressure tactics that misstate urgency.

## Output

Deliver a **case statement**.

- Purpose of this case statement, in two sentences.
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

Amira Hassan, program director at Open Kitchen Society in Calgary, needs a case statement by 30 September 2026. A case says 90 percent of participants succeed, and no outcome is tracked.

### Example data

```text
From: Amira Hassan, program director
Organization: Open Kitchen Society, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A case says 90 percent of participants succeed, and no outcome is tracked.

The need they can evidence: one PDF, 2 pages, dated 14 September 2026
The program: Literacy program, recorded 14 September 2026. No supporting file attached
The ask: A case says 90 percent of participants succeed, and no outcome is tracked. Stated once, in the ask. Not written down anywhere else
What donors must not be told: Donor list segment B, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Case statement**
To: Amira Hassan, program director, Open Kitchen Society
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the percentage and describes the program without a fake rate.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The need they can evidence | one PDF, 2 pages, dated 14 September 2026 | Needs confirmation |
| The program | Literacy program, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The ask | A case says 90 percent of participants succeed, and no outcome is tracked. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| What donors must not be told | Donor list segment B, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Describe the need with evidence they have**

**2. Explain what the program actually does**

**3. Separate outputs from outcomes**

**4. Make one ask**

**5. Do not invent a beneficiary story or a success rate**

**Deliberately not done**
- Invented beneficiary stories.
- A fake urgency.
- Outcomes they have not measured.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Amira Hassan by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented beneficiary stories
- A fake urgency
- Outcomes they have not measured

## Related skills

- `grant-narrative`
- `marketing-claims-review`
