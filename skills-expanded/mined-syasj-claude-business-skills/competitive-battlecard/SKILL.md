---
name: competitive-battlecard
description: "Build a battlecard from proof and trap questions, without invented competitor weaknesses. Use when the user mentions battlecard, competitive card, versus competitor, displacement notes, or asks for a competitive battlecard. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'competitive-battlecard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Competitive Battlecard

Build a battlecard from proof and trap questions, without invented competitor weaknesses.

## When to use this skill

Use this skill when the user:

- battlecard
- competitive card
- versus competitor
- displacement notes

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

- The competitor or alternative, including the status quo
- Facts the user can source
- Where you honestly lose
- Proof points

## Workflow


### 1. Name the alternative

Include do-nothing or spreadsheets if that is who you lose to.
### 2. Facts only

Product differences the user can support. Mark rumors as rumors and do not put them in the talk track.
### 3. Where we lose

The buyer for whom the alternative is a better fit. Reps need permission to walk.
### 4. Trap questions

Questions that reveal fit, not questions designed to humiliate a rival.
### 5. Proof

The asset that backs each claim. No asset, no claim.
### 6. Landmines

What not to say, including unshipped features and unverified insults.

## Output

Deliver a **competitive battlecard**.

- Purpose of this competitive battlecard, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a competitive battlecard by 30 September 2026. Reps claim a rival 'is going out of business' with no source.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Reps claim a rival 'is going out of business' with no source.

The competitor or alternative, including the status quo: two deals cited from memory. Neither has a written loss reason
Facts the user can source: note from Samir Qureshi, 14 September 2026. No outside report
Where you honestly lose: two deals cited from memory. Neither has a written loss reason
Proof points: one customer email, 14 September 2026, no attachment beyond that
```

### Example outcome

**Competitive battlecard**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Deletes the rumor, states a sourced product difference, and names the segment where the rival is a better fit.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The competitor or alternative, including the status quo | two deals cited from memory. Neither has a written loss reason | Needs confirmation |
| Facts the user can source | note from Samir Qureshi, 14 September 2026. No outside report | Carried into the draft |
| Where you honestly lose | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| Proof points | one customer email, 14 September 2026, no attachment beyond that | Needs confirmation |

**How this draft was built**

**1. Name the alternative**  
Include do-nothing or spreadsheets if that is who you lose to.

**2. Facts only**  
Product differences the user can support. Mark rumors as rumors and do not put them in the talk track.

**3. Where we lose**  
The buyer for whom the alternative is a better fit. Reps need permission to walk.

**4. Trap questions**  
Questions that reveal fit, not questions designed to humiliate a rival.

**5. Proof**  
The asset that backs each claim. No asset, no claim.

**Deliberately not done**
- Invented competitor revenue or roadmap.
- Insults with no proof.
- Hiding the segment where you lose.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented competitor revenue or roadmap.
- Insults with no proof.
- Hiding the segment where you lose.

## Related skills

- `competitive-strategy`
- `objection-handling`
