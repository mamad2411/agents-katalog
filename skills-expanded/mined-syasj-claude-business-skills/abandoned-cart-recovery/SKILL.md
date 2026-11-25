---
name: abandoned-cart-recovery
description: "Draft a cart recovery email sequence that reminds without pressuring and states what was in the cart. Use when the user mentions abandoned cart email, cart recovery, checkout abandonment, basket reminder, or asks for a cart recovery email. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'abandoned-cart-recovery' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Abandoned Cart Recovery

Draft a cart recovery email sequence that reminds without pressuring and states what was in the cart.

## When to use this skill

Use this skill when the user:

- abandoned cart email
- cart recovery
- checkout abandonment
- basket reminder

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

- What was in the cart
- The price
- Any stock constraint that is real
- Timing they want

## Workflow


### 1. Step 1

State exactly what was in the cart. Do not guess what they wanted.
### 2. Step 2

A real stock constraint is a fact, not a pressure tactic. Do not invent scarcity.
### 3. Step 3

One reminder before a discount. Do not open with a discount.
### 4. Step 4

If a discount is offered, make the terms clear and honor them.
### 5. Step 5

Do not send more than three emails in a sequence without the shopper's prior consent.

## Output

Deliver a **cart recovery email**.

- Purpose of this cart recovery email, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs a cart recovery email by 30 September 2026. A sequence says "only 2 left" when the warehouse has 400 units.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A sequence says "only 2 left" when the warehouse has 400 units.

What was in the cart: Returns desk log, last reviewed 14 September 2026. No owner named since
The price: CAD 120
Any stock constraint that is real: no extra headcount, and no result that is not in this file
Timing they want: End-cap display 3. Partly documented: the what is written down, the who is not
```

### Example outcome

**Cart recovery email — draft ready to send**

> To: the recipient named in the file
> From: Diane Cho, store lead, Harbor Goods
> Date: 14 September 2026

---

Hello,

Removes the false scarcity and earns the second email with a useful reminder.

Everything above comes from the file dated 14 September 2026. Where a figure, a date, or a commitment was not in that file, this note leaves it out rather than filling the gap.

One point is still open, and I would rather flag it than paper over it. I will confirm it before 30 September 2026 and follow up either way.

Diane Cho
store lead, Harbor Goods

---

**How this draft was checked**

1. **State exactly what was in the cart. Do not guess what they wanted**
2. **A real stock constraint is a fact, not a pressure tactic. Do not invent scarcity**
3. **One reminder before a discount. Do not open with a discount**
4. **If a discount is offered, make the terms clear and honor them**

**Deliberately not done**
- Invented scarcity.
- A discount on touch one.
- More emails than agreed.

Next: Diane Cho sends after confirming the open point. Due 30 September 2026. This is a draft, not a sent message.

## Anti-patterns

- Invented scarcity
- A discount on touch one
- More emails than agreed

## Related skills

- `promotion-review`
