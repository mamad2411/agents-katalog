---
name: break-even-analysis
description: "Find the volume or price where a defined contribution covers a defined fixed cost, and show the assumption that matters. Use when the user mentions break even, breakeven, how many do we need to sell, contribution versus fixed cost, or asks for a break-even note. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'break-even-analysis' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Break-Even Analysis

Find the volume or price where a defined contribution covers a defined fixed cost, and show the assumption that matters.

## When to use this skill

Use this skill when the user:

- break even
- breakeven
- how many do we need to sell
- contribution versus fixed cost

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

- Price and variable cost per unit
- Which costs are fixed over the horizon
- The horizon
- Capacity limits

## Workflow


### 1. Define the box

The product or location, and the months the fixed cost stays fixed. Break-even without a box is a slogan.
### 2. Compute contribution per unit

Price minus variable cost, using the user's figures. If contribution is zero or negative, say break-even does not exist at this price.
### 3. Divide fixed cost by contribution

Show the units and the revenue. Round only at the end, and say you rounded.
### 4. Apply capacity

If the break-even volume exceeds capacity, the answer is that the cost structure does not fit, not a pep talk.
### 5. Sensitivity

The variable that moves the answer most. One chart's worth of prose is enough.
### 6. Do not add a profit goal silently

If the user wants a target profit, show it as a separate line.

## Output

Deliver a **break-even note**.

- Purpose of this break-even note, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a break-even note by 30 September 2026. A cafe owner wants to know how many days of a new catering offer it takes to cover a hired cook.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A cafe owner wants to know how many days of a new catering offer it takes to cover a hired cook.

Price and variable cost per unit: CAD 180
Which costs are fixed over the horizon: 13 weeks
The horizon: 13 weeks
Capacity limits: two people, no overtime figure
```

### Example outcome

**Break-even note**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A break-even quantity inside a stated time box, with the capacity check and the dominant assumption labeled.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Price and variable cost per unit | CAD 180 | Needs confirmation |
| Which costs are fixed over the horizon | 13 weeks | Carried into the draft |
| The horizon | 13 weeks | Carried into the draft |
| Capacity limits | two people, no overtime figure | Needs confirmation |

**How this draft was built**

**1. Define the box**  
The product or location, and the months the fixed cost stays fixed. Break-even without a box is a slogan.

**2. Compute contribution per unit**  
Price minus variable cost, using the user's figures. If contribution is zero or negative, say break-even does not exist at this price.

**3. Divide fixed cost by contribution**  
Show the units and the revenue. Round only at the end, and say you rounded.

**4. Apply capacity**  
If the break-even volume exceeds capacity, the answer is that the cost structure does not fit, not a pep talk.

**5. Sensitivity**  
The variable that moves the answer most. One chart's worth of prose is enough.

**Deliberately not done**
- Treating all costs as variable.
- Ignoring a capacity ceiling.
- A break-even point with no time box.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Treating all costs as variable.
- Ignoring a capacity ceiling.
- A break-even point with no time box.

## Related skills

- `unit-economics`
- `pricing-margin-bridge`
- `capex-business-case`
