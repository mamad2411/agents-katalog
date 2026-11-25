---
name: offer-comparison
description: "Compare property offers on the terms the user cares about, without advising which legal form to sign. Use when the user mentions compare offers, property offers, which offer, offer matrix, or asks for a offer comparison. Real estate skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: real-estate
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'offer-comparison' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Offer Comparison

Compare property offers on the terms the user cares about, without advising which legal form to sign.

## When to use this skill

Use this skill when the user:

- compare offers
- property offers
- which offer
- offer matrix

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not brokerage, appraisal, or legal advice. Do not invent comparable sales, rents, or legal rights. A licensed local professional must confirm any transaction.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The offers
- The seller or buyer priorities
- Deadlines they stated
- Contingencies visible in the offers

## Workflow


### 1. Step 1

Build a matrix of price, timing, contingencies, and costs they can see.
### 2. Step 2

Rank only on priorities they named.
### 3. Step 3

Do not invent a buyer's financing strength.
### 4. Step 4

Flag a deadline that needs a professional response.
### 5. Step 5

Recommend questions, not a signature.
### 6. Step 6

A licensed local professional must confirm the transaction.

## Output

Deliver a **offer comparison**.

- Purpose of this offer comparison, in two sentences.
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

Helen Cho, property manager at Cedar Street Properties in Airdrie, needs an offer comparison by 30 September 2026. One offer is higher but waives an inspection the seller has not disclosed defects for.

### Example data

```text
From: Helen Cho, property manager
Organization: Cedar Street Properties, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

One offer is higher but waives an inspection the seller has not disclosed defects for.

The offers: CAD 79, dates not set, cap not set
The seller or buyer priorities: Unit 4B lease, recorded 14 September 2026. No supporting file attached
Deadlines they stated: 30 September 2026
Contingencies visible in the offers: CAD 79, dates not set, cap not set
```

### Example outcome

**Offer comparison**
To: Helen Cho, property manager, Cedar Street Properties
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows the inspection gap and leaves the signature to the principal and their professional.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The offers | CAD 79, dates not set, cap not set | Needs confirmation |
| The seller or buyer priorities | Unit 4B lease, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Deadlines they stated | 30 September 2026 | Carried into the draft |
| Contingencies visible in the offers | CAD 79, dates not set, cap not set | Needs confirmation |

**How this draft was built**

**1. Build a matrix of price, timing, contingencies, and costs they can see**

**2. Rank only on priorities they named**

**3. Do not invent a buyer's financing strength**

**4. Flag a deadline that needs a professional response**

**5. Recommend questions, not a signature**

**Deliberately not done**
- Invented financing strength.
- A signature recommendation.
- Hidden contingencies.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Helen Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented financing strength
- A signature recommendation
- Hidden contingencies

## Related skills

- `property-due-diligence`
- `decision-log`
