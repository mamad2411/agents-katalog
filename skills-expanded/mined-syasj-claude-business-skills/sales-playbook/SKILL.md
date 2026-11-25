---
name: sales-playbook
description: "Write one sales play for a repeated situation, with talk track, proof, and exit criteria. Use when the user mentions sales playbook, sales play, talk track, how we sell this, or asks for a sales play. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sales-playbook' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sales Playbook

Write one sales play for a repeated situation, with talk track, proof, and exit criteria.

## When to use this skill

Use this skill when the user:

- sales playbook
- sales play
- talk track
- how we sell this

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The situation the play covers
- The buyer
- Proof
- The stage exit

## Workflow


### 1. Situation

One trigger, such as a renewal risk or a competitive displacement. Do not write a play for 'selling'.
### 2. Entry and exit

When a rep uses the play, and what evidence ends it.
### 3. Talk track

Questions first, then a short narrative. Claims must be supportable.
### 4. Assets

The one-pager or demo scene they should use. Do not link imaginary assets.
### 5. Landmines

What not to say, including roadmap promises and competitor insults.
### 6. Coaching

How a manager knows the play was run, from notes, not from vibes.

## Output

Deliver a **sales play**.

- Purpose of this sales play, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a sales play by 30 September 2026. Reps keep promising a feature that is not shipped when they hear a competitor's name.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Reps keep promising a feature that is not shipped when they hear a competitor's name.

The situation the play covers: Harbor Goods, recorded 14 September 2026. No supporting file attached
The buyer: Redline Parts
Proof: one customer email, 14 September 2026, no attachment beyond that
The stage exit: Harbor Goods, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Sales play**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A competitive play with a question track, a ban on unshipped features, and an exit criterion based on buyer criteria.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The situation the play covers | Harbor Goods, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The buyer | Redline Parts | Carried into the draft |
| Proof | one customer email, 14 September 2026, no attachment beyond that | Carried into the draft |
| The stage exit | Harbor Goods, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Situation**  
One trigger, such as a renewal risk or a competitive displacement. Do not write a play for 'selling'.

**2. Entry and exit**  
When a rep uses the play, and what evidence ends it.

**3. Talk track**  
Questions first, then a short narrative. Claims must be supportable.

**4. Assets**  
The one-pager or demo scene they should use. Do not link imaginary assets.

**5. Landmines**  
What not to say, including roadmap promises and competitor insults.

**Deliberately not done**
- A playbook that is a product manual.
- Unsupported claims in the talk track.
- No exit criterion.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A playbook that is a product manual.
- Unsupported claims in the talk track.
- No exit criterion.

## Related skills

- `demo-storyboard`
- `competitive-battlecard`
