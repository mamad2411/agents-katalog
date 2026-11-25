---
name: promotion-review
description: "Review a promotion for margin, inventory, and honest terms. Use when the user mentions promotion review, retail promo, discount event, offer review retail, or asks for a promotion review. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'promotion-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Promotion Review

Review a promotion for margin, inventory, and honest terms.

## When to use this skill

Use this skill when the user:

- promotion review
- retail promo
- discount event
- offer review retail

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent inventory, prices, or reviews. Do not write deceptive promotions.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The offer terms
- Margin they can show
- Inventory
- Customer-facing rules

## Workflow


### 1. Step 1

State the terms a shopper will see.
### 2. Step 2

Check margin from their cost. If cost is missing, say so.
### 3. Step 3

Confirm inventory can support the advertised depth.
### 4. Step 4

No fake was-prices or fake end times.
### 5. Step 5

Define the exception path for rain checks if they offer them.
### 6. Step 6

Name the owner who stops the promo if terms cannot be honored.

## Output

Deliver a **promotion review**.

- Purpose of this promotion review, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs a promotion review by 30 September 2026. A banner shows a crossed-out price the item never sold for.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A banner shows a crossed-out price the item never sold for.

The offer terms: CAD 79, dates not set, cap not set
Margin they can show: End-cap display 3, recorded 14 September 2026. No supporting file attached
Inventory: 70 on hand
Customer-facing rules: Kite Freight
```

### Example outcome

**Promotion review**
To: Diane Cho, store lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the crossed-out price and checks inventory before the banner runs.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The offer terms | CAD 79, dates not set, cap not set | Needs confirmation |
| Margin they can show | End-cap display 3, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Inventory | 70 on hand | Carried into the draft |
| Customer-facing rules | Kite Freight | Needs confirmation |

**How this draft was built**

**1. State the terms a shopper will see**

**2. Check margin from their cost. If cost is missing, say so**

**3. Confirm inventory can support the advertised depth**

**4. No fake was-prices or fake end times**

**5. Define the exception path for rain checks if they offer them**

**Deliberately not done**
- Fake was-prices.
- Advertising stock they do not have.
- Hidden exclusions.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Fake was-prices
- Advertising stock they do not have
- Hidden exclusions

## Related skills

- `offer-design`
- `marketing-claims-review`
