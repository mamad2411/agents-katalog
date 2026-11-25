---
name: board-fundraising-report
description: "Report fundraising progress with cash received, pledges, and restrictions kept distinct. Use when the user mentions fundraising report, donor report, campaign progress, gift report, or asks for a fundraising report. Nonprofit and public interest skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: nonprofit
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'board-fundraising-report' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Fundraising Report

Report fundraising progress with cash received, pledges, and restrictions kept distinct.

## When to use this skill

Use this skill when the user:

- fundraising report
- donor report
- campaign progress
- gift report

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

- Cash received
- Pledges
- Restrictions
- The goal

## Workflow


### 1. Step 1

Separate cash from pledges.
### 2. Step 2

Note restrictions that limit use.
### 3. Step 3

Compare to the goal they set.
### 4. Step 4

Do not count a verbal maybe as a pledge.
### 5. Step 5

Name the pipeline only with evidence.
### 6. Step 6

No individual donor's private details beyond what the user said may be shared.

## Output

Deliver a **fundraising report**.

- Purpose of this fundraising report, in two sentences.
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

Amira Hassan, program director at Open Kitchen Society in Calgary, needs a fundraising report by 30 September 2026. A report counts a dinner conversation as committed revenue.

### Example data

```text
From: Amira Hassan, program director
Organization: Open Kitchen Society, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A report counts a dinner conversation as committed revenue.

Cash received: Donor list segment B. Partly documented: the what is written down, the who is not
Pledges: Donor list segment B, last reviewed 14 September 2026. No owner named since
Restrictions: Literacy program, last reviewed 14 September 2026. No owner named since
The goal: A report counts a dinner conversation as committed revenue. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Fundraising report**
To: Amira Hassan, program director, Open Kitchen Society
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Moves the conversation to a prospect note and keeps cash and pledges apart.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Cash received | Donor list segment B. Partly documented: the what is written down, the who is not | Needs confirmation |
| Pledges | Donor list segment B, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Restrictions | Literacy program, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The goal | A report counts a dinner conversation as committed revenue. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. Separate cash from pledges**

**2. Note restrictions that limit use**

**3. Compare to the goal they set**

**4. Do not count a verbal maybe as a pledge**

**5. Name the pipeline only with evidence**

**Deliberately not done**
- Maybes counted as pledges.
- Restricted gifts shown as unrestricted.
- Private details overshared.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Amira Hassan by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Maybes counted as pledges
- Restricted gifts shown as unrestricted
- Private details overshared

## Related skills

- `cash-flow-forecast`
- `nonprofit-case-statement`
