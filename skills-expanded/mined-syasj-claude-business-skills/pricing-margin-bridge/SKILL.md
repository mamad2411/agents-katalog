---
name: pricing-margin-bridge
description: "Trace price, mix, and cost so a margin change has a cause and a commercial response. Use when the user mentions margin bridge, price mix cost, why did margin fall, pricing review, or asks for a price-mix-cost bridge. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pricing-margin-bridge' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Pricing and Margin Bridge

Trace price, mix, and cost so a margin change has a cause and a commercial response.

## When to use this skill

Use this skill when the user:

- margin bridge
- price mix cost
- why did margin fall
- pricing review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not investment, tax, or financial advice. Do not invent rates of return, tax rates, or valuation multiples. A qualified finance professional must review any decision that moves money.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Revenue and cost for two periods
- Price and volume detail if available
- Known mix shifts
- Discount or rebate practice

## Workflow


### 1. Start with the margin change

State gross margin or contribution change in the user's currency and in points.
### 2. Separate price, volume, and mix

Use the detail the user has. If mix cannot be seen, say the bridge is incomplete rather than forcing a fake split.
### 3. Put discounts in price

A discount is a price decision. Do not hide it in cost.
### 4. Isolate cost inflation

Input cost changes sit on their own step, with the user's evidence.
### 5. Recommend one commercial move

A price test, a mix target, or a cost action. Not all three at full strength unless the user has capacity.
### 6. Flag customer impact

Who would feel the move. Do not draft deceptive pricing.

## Output

Deliver a **price-mix-cost bridge**.

- Purpose of this price-mix-cost bridge, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a price-mix-cost bridge by 30 September 2026. Gross margin fell two points and sales says it was only product mix.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Gross margin fell two points and sales says it was only product mix.

Revenue and cost for two periods: month ending 14 September 2026
Price and volume detail if available: CAD 180
Known mix shifts: Harbor & Co receipt. Stated in the ask, not documented anywhere else
Discount or rebate practice: 55 in the last period. No prior period attached, so no trend
```

### Example outcome

**Price-mix-cost bridge**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows what portion is mix, price, and cost on the available data, plus one commercial response.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Revenue and cost for two periods | month ending 14 September 2026 | Needs confirmation |
| Price and volume detail if available | CAD 180 | Carried into the draft |
| Known mix shifts | Harbor & Co receipt. Stated in the ask, not documented anywhere else | Carried into the draft |
| Discount or rebate practice | 55 in the last period. No prior period attached, so no trend | Needs confirmation |

**How this draft was built**

**1. Start with the margin change**  
State gross margin or contribution change in the user's currency and in points.

**2. Separate price, volume, and mix**  
Use the detail the user has. If mix cannot be seen, say the bridge is incomplete rather than forcing a fake split.

**3. Put discounts in price**  
A discount is a price decision. Do not hide it in cost.

**4. Isolate cost inflation**  
Input cost changes sit on their own step, with the user's evidence.

**5. Recommend one commercial move**  
A price test, a mix target, or a cost action. Not all three at full strength unless the user has capacity.

**Deliberately not done**
- A margin story with no bridge.
- Blaming mix when the data cannot show mix.
- Recommending a price increase with no customer consequence.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A margin story with no bridge.
- Blaming mix when the data cannot show mix.
- Recommending a price increase with no customer consequence.

## Related skills

- `unit-economics`
- `pricing-packaging`
- `budget-variance-review`
