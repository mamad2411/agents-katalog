---
name: meeting-notes
description: "Write meeting notes that capture decisions, owners, and open questions. Use when the user mentions meeting notes, minutes, action items, notes from the call, or asks for a meeting notes. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'meeting-notes' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Meeting Notes

Write meeting notes that capture decisions, owners, and open questions.

## When to use this skill

Use this skill when the user:

- meeting notes
- minutes
- action items
- notes from the call

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Productivity systems serve the person's actual constraints. Do not recommend surveillance of colleagues or hidden monitoring.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The purpose
- Decisions heard
- Owners
- Open questions

## Workflow


### 1. Step 1

Start with the purpose and the date.
### 2. Step 2

Record decisions separately from discussion.
### 3. Step 3

Each action has an owner and a date, or it is not an action.
### 4. Step 4

Mark unclear points as questions. Do not invent consensus.
### 5. Step 5

Keep confidential items out of a note that will be widely shared.
### 6. Step 6

Send the note to the people who must act, if the user asks for a distribution list they control.

## Output

Deliver a **meeting notes**.

- Purpose of this meeting notes, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a meeting notes by 30 September 2026. Notes say the team agreed though two people dissented.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Notes say the team agreed though two people dissented.

The purpose: Notes say the team agreed though two people dissented. Stated once, in the ask. Not written down anywhere else
Decisions heard: Notes say the team agreed though two people dissented
Owners: Mara Chen, founder
Open questions: Notes say the team agreed though two people dissented
```

### Example outcome

**Meeting notes**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Notes that record the dissent and assign owners only to real actions.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The purpose | Notes say the team agreed though two people dissented. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Decisions heard | Notes say the team agreed though two people dissented | Carried into the draft |
| Owners | Mara Chen, founder | Carried into the draft |
| Open questions | Notes say the team agreed though two people dissented | Needs confirmation |

**How this draft was built**

**1. Start with the purpose and the date**

**2. Record decisions separately from discussion**

**3. Each action has an owner and a date, or it is not an action**

**4. Mark unclear points as questions. Do not invent consensus**

**5. Keep confidential items out of a note that will be widely shared**

**Deliberately not done**
- Invented consensus.
- Actions with no owner.
- Confidential details in a broad note.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented consensus
- Actions with no owner
- Confidential details in a broad note

## Related skills

- `board-meeting-facilitator`
- `decision-log`
