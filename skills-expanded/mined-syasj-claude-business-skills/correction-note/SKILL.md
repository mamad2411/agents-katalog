---
name: correction-note
description: "Draft a correction that states what was wrong, what is right, and where it ran. Use when the user mentions correction, retraction note, fix a published error, correction wording, or asks for a correction. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'correction-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Correction Note

Draft a correction that states what was wrong, what is right, and where it ran.

## When to use this skill

Use this skill when the user:

- correction
- retraction note
- fix a published error
- correction wording

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

- The original claim
- The correct fact
- Where it appeared
- Who must approve

## Workflow


### 1. Step 1

State the error plainly.
### 2. Step 2

State the correct fact they can support.
### 3. Step 3

Say where the error appeared.
### 4. Step 4

Do not bury the correction in a new story.
### 5. Step 5

Note if a quote was wrong. Do not quietly rewrite history.
### 6. Step 6

Mark the draft for the editor to approve.

## Output

Deliver a **correction**.

- Purpose of this correction, in two sentences.
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

Jonah Ellis, assignment editor at Foothills Desk in Calgary, needs a correction by 30 September 2026. A correction draft says 'updated for clarity' when a number was wrong.

### Example data

```text
From: Jonah Ellis, assignment editor
Organization: Foothills Desk, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A correction draft says 'updated for clarity' when a number was wrong.

The original claim: the draft sentence is broader than the note
The correct fact: Plant turnaround, recorded 14 September 2026. No supporting file attached
Where it appeared: Fare change, recorded 14 September 2026. No supporting file attached
Who must approve: Jonah Ellis, assignment editor
```

### Example outcome

**Correction**
To: Jonah Ellis, assignment editor, Foothills Desk
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Says the number was wrong and gives the supported figure.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The original claim | the draft sentence is broader than the note | Needs confirmation |
| The correct fact | Plant turnaround, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Where it appeared | Fare change, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Who must approve | Jonah Ellis, assignment editor | Needs confirmation |

**How this draft was built**

**1. State the error plainly**

**2. State the correct fact they can support**

**3. Say where the error appeared**

**4. Do not bury the correction in a new story**

**5. Note if a quote was wrong. Do not quietly rewrite history**

**Deliberately not done**
- A buried correction.
- A rewritten quote with no note.
- An unsupported replacement fact.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Ellis by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A buried correction
- A rewritten quote with no note
- An unsupported replacement fact

## Related skills

- `marketing-claims-review`
- `editorial-brief`
