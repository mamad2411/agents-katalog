---
name: schedule-look-ahead
description: "Build a short look-ahead from constraints, not from a hopeful bar chart. Use when the user mentions look-ahead, three-week look-ahead, constraint schedule, weekly work plan, or asks for a look-ahead. Construction skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: construction
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'schedule-look-ahead' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Schedule Look-Ahead

Build a short look-ahead from constraints, not from a hopeful bar chart.

## When to use this skill

Use this skill when the user:

- look-ahead
- three-week look-ahead
- constraint schedule
- weekly work plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Site safety and contract administration follow the contract and the site rules. Do not tell anyone to skip a safety control. Do not invent quantities.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Planned activities
- Constraints: design, material, access
- Crew available
- Inspections

## Workflow


### 1. Step 1

List activities the constraints actually allow.
### 2. Step 2

Mark activities blocked by a missing RFI, material, or inspection.
### 3. Step 3

Match crew to the allowed work.
### 4. Step 4

Do not show blocked work as committed.
### 5. Step 5

Identify the constraint to remove next.
### 6. Step 6

Update from yesterday's actuals they supplied.

## Output

Deliver a **look-ahead**.

- Purpose of this look-ahead, in two sentences.
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

Tom Reilly, site lead at Birch Siteworks in Cochrane, needs a look-ahead by 30 September 2026. A look-ahead schedules a pour before the inspection the city requires.

### Example data

```text
From: Tom Reilly, site lead
Organization: Birch Siteworks, Cochrane
Date: 14 September 2026
Needed by: 30 September 2026

A look-ahead schedules a pour before the inspection the city requires.

Planned activities: Two-week look-ahead. Stated in the ask, not documented anywhere else
Constraints: design, material, access: design: in the file; material: not in the file; access: open
Crew available: Two-week look-ahead, recorded 14 September 2026. No supporting file attached
Inspections: Two-week look-ahead. Stated in the ask, not documented anywhere else
```

### Example outcome

**Look-ahead**
To: Tom Reilly, site lead, Birch Siteworks
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Parks the pour behind the inspection and names the constraint owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Planned activities | Two-week look-ahead. Stated in the ask, not documented anywhere else | Needs confirmation |
| Constraints: design, material, access | design: in the file; material: not in the file; access: open | Carried into the draft |
| Crew available | Two-week look-ahead, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Inspections | Two-week look-ahead. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. List activities the constraints actually allow**

**2. Mark activities blocked by a missing RFI, material, or inspection**

**3. Match crew to the allowed work**

**4. Do not show blocked work as committed**

**5. Identify the constraint to remove next**

**Deliberately not done**
- Blocked work shown as committed.
- No constraint column.
- A look-ahead that ignores yesterday.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Tom Reilly by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Blocked work shown as committed
- No constraint column
- A look-ahead that ignores yesterday

## Related skills

- `production-schedule`
- `site-daily-report`
