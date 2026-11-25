---
name: editorial-calendar-newsroom
description: "Plan a newsroom or content desk day around the stories that are ready and the slots that should stay empty. Use when the user mentions newsroom planning, desk plan, what do we run, editorial meeting, or asks for a planning note. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'editorial-calendar-newsroom' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Newsroom Planning Note

Plan a newsroom or content desk day around the stories that are ready and the slots that should stay empty.

## When to use this skill

Use this skill when the user:

- newsroom planning
- desk plan
- what do we run
- editorial meeting

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate quotes, sources, or images. Label opinion. Do not draft impersonation or defamation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Ready stories
- Open reporting
- Slots
- Legal or standards flags

## Workflow


### 1. Step 1

Run only stories with a sourced point.
### 2. Step 2

Leave a slot empty rather than fill it with an unsourced piece.
### 3. Step 3

Flag legal review where they said it is required.
### 4. Step 4

Separate opinion from news in the plan.
### 5. Step 5

Do not assign a story that requires deception to report.
### 6. Step 6

Name the editor for each slot.

## Output

Deliver a **planning note**.

- Purpose of this planning note, in two sentences.
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

Jonah Ellis, assignment editor at Foothills Desk in Calgary, needs a planning note by 30 September 2026. The plan assigns a trend piece with no sources because the slot is empty.

### Example data

```text
From: Jonah Ellis, assignment editor
Organization: Foothills Desk, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The plan assigns a trend piece with no sources because the slot is empty.

Ready stories: Company statement. Stated in the ask, not documented anywhere else
Open reporting: one file, dated 14 September 2026. No earlier version attached for comparison
Slots: Fare change. Partly documented: the what is written down, the who is not
Legal or standards flags: their one-page rule dated 2 Mar 2026. No exception log since
```

### Example outcome

**Planning note**
To: Jonah Ellis, assignment editor, Foothills Desk
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Kills or holds the piece and leaves the slot open.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Ready stories | Company statement. Stated in the ask, not documented anywhere else | Needs confirmation |
| Open reporting | one file, dated 14 September 2026. No earlier version attached for comparison | Carried into the draft |
| Slots | Fare change. Partly documented: the what is written down, the who is not | Carried into the draft |
| Legal or standards flags | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |

**How this draft was built**

**1. Run only stories with a sourced point**

**2. Leave a slot empty rather than fill it with an unsourced piece**

**3. Flag legal review where they said it is required**

**4. Separate opinion from news in the plan**

**5. Do not assign a story that requires deception to report**

**Deliberately not done**
- Filling a slot with an unsourced piece.
- Opinion labeled as news.
- A deceptive reporting assignment.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Ellis by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Filling a slot with an unsourced piece
- Opinion labeled as news
- A deceptive reporting assignment

## Related skills

- `content-calendar`
- `editorial-brief`
