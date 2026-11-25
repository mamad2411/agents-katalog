---
name: proposal-writer
description: "Write a proposal that restates the buyer's problem, the offer, the proof, and the ask, without invented ROI. Use when the user mentions write a proposal, sales proposal, statement of work narrative, proposal draft, or asks for a customer proposal. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'proposal-writer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Proposal Writer

Write a proposal that restates the buyer's problem, the offer, the proof, and the ask, without invented ROI.

## When to use this skill

Use this skill when the user:

- write a proposal
- sales proposal
- statement of work narrative
- proposal draft

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

- The buyer's stated problem
- The offer and what is out of scope
- Proof you actually have
- Price and terms the user can stand behind

## Workflow


### 1. Mirror the problem

Use the buyer's language from discovery. If discovery was thin, say the proposal is premature.
### 2. Offer

What you will do, by when, and what you will not do. Ambiguous scope is a future dispute.
### 3. Proof

Only case facts the user supplied. No invented percentages.
### 4. Commercials

Price, term, and assumptions. Do not hide a material condition in a footnote.
### 5. Ask

The decision and the date. A proposal with no ask is a brochure.
### 6. Review

Flag claims that need the marketing-claims skill or counsel. Do not overpromise implementation.

## Output

Deliver a **customer proposal**.

- Purpose of this customer proposal, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a customer proposal by 30 September 2026. A seller wants a proposal for a buyer who has not confirmed the problem or the budget.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A seller wants a proposal for a buyer who has not confirmed the problem or the budget.

The buyer's stated problem: A seller wants a proposal for a buyer who has not confirmed the problem or the budget. Stated once, in the ask. Not written down anywhere else
The offer and what is out of scope: anything not named in the ask
Proof you actually have: one customer email, 14 September 2026, no attachment beyond that
Price and terms the user can stand behind: CAD 180
```

### Example outcome

**Customer proposal**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses invented ROI and lists the two facts still required before price is presented as final.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The buyer's stated problem | A seller wants a proposal for a buyer who has not confirmed the problem or the budget. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The offer and what is out of scope | anything not named in the ask | Carried into the draft |
| Proof you actually have | one customer email, 14 September 2026, no attachment beyond that | Carried into the draft |
| Price and terms the user can stand behind | CAD 180 | Needs confirmation |

**How this draft was built**

**1. Mirror the problem**  
Use the buyer's language from discovery. If discovery was thin, say the proposal is premature.

**2. Offer**  
What you will do, by when, and what you will not do. Ambiguous scope is a future dispute.

**3. Proof**  
Only case facts the user supplied. No invented percentages.

**4. Commercials**  
Price, term, and assumptions. Do not hide a material condition in a footnote.

**5. Ask**  
The decision and the date. A proposal with no ask is a brochure.

**Deliberately not done**
- A ROI slide built from invented savings.
- Scope described only as 'full service'.
- A proposal written before the problem is known.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A ROI slide built from invented savings.
- Scope described only as 'full service'.
- A proposal written before the problem is known.

## Related skills

- `discovery-call`
- `pricing-negotiation`
