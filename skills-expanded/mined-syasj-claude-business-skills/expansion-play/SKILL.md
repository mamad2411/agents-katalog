---
name: expansion-play
description: "Design an expansion conversation that starts from a realized outcome, not from the seller's quota gap. Use when the user mentions upsell, expansion play, cross-sell, grow the account, or asks for a expansion play. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'expansion-play' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Expansion Play

Design an expansion conversation that starts from a realized outcome, not from the seller's quota gap.

## When to use this skill

Use this skill when the user:

- upsell
- expansion play
- cross-sell
- grow the account

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

- The outcome already achieved
- The next problem the customer has named
- Stakeholders
- Products that honestly fit

## Workflow


### 1. Evidence of value

What they already got. If value is unproven, the play is adoption, not expansion.
### 2. Next problem

Use a problem they named. Do not invent a department's pain.
### 3. Fit

Which offer matches that problem, and what is a bad fit. Say the bad fit out loud.
### 4. Stakeholders

Who owns the next problem. The original buyer may be the wrong room.
### 5. Commercial path

How pricing works, using real packaging. No surprise bundle.
### 6. Timing

Tie the ask to their calendar, not only to your quarter end.

## Output

Deliver a **expansion play**.

- Purpose of this expansion play, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs an expansion play by 30 September 2026. A rep wants to cross-sell a second module, but the first module has no confirmed outcome.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A rep wants to cross-sell a second module, but the first module has no confirmed outcome.

The outcome already achieved: A rep wants to cross-sell a second module, but the first module has no confirmed outcome. Stated once, in the ask. Not written down anywhere else
The next problem the customer has named: A rep wants to cross-sell a second module, but the first module has no confirmed outcome. Stated once, in the ask. Not written down anywhere else
Stakeholders: Samir Qureshi plus two others named in the thread. No distribution list attached
Products that honestly fit: Harbor Goods. Stated in the ask, not documented anywhere else
```

### Example outcome

**Expansion play**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Pauses expansion and defines the adoption proof required before a second offer is made.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcome already achieved | A rep wants to cross-sell a second module, but the first module has no confirmed outcome. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The next problem the customer has named | A rep wants to cross-sell a second module, but the first module has no confirmed outcome. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Stakeholders | Samir Qureshi plus two others named in the thread. No distribution list attached | Carried into the draft |
| Products that honestly fit | Harbor Goods. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Evidence of value**  
What they already got. If value is unproven, the play is adoption, not expansion.

**2. Next problem**  
Use a problem they named. Do not invent a department's pain.

**3. Fit**  
Which offer matches that problem, and what is a bad fit. Say the bad fit out loud.

**4. Stakeholders**  
Who owns the next problem. The original buyer may be the wrong room.

**5. Commercial path**  
How pricing works, using real packaging. No surprise bundle.

**Deliberately not done**
- Expanding before value is real.
- Inventing a new department's pain.
- Quarter-end pressure as the only timing logic.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Expanding before value is real.
- Inventing a new department's pain.
- Quarter-end pressure as the only timing logic.

## Related skills

- `account-plan`
- `customer-health-score`
