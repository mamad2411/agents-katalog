---
name: unit-economics
description: "Calculate contribution economics for one real unit the business sells, and show which assumption dominates. Use when the user mentions unit economics, contribution margin, CAC payback, do we make money per customer, or asks for a unit economics sheet. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'unit-economics' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Unit Economics

Calculate contribution economics for one real unit the business sells, and show which assumption dominates.

## When to use this skill

Use this skill when the user:

- unit economics
- contribution margin
- CAC payback
- do we make money per customer

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

- The unit: customer, order, location, or contract
- Price and direct costs the user can support
- Acquisition cost definition
- Retention or repeat evidence, if any

## Workflow


### 1. Define the unit

Say exactly what one unit is. Mixing orders and customers in one margin is how teams fool themselves.
### 2. Build contribution

Price minus costs that vary with the unit. Keep fixed overhead out of the unit and show it separately.
### 3. Treat acquisition honestly

Include the costs the user says are required to win the unit. Do not ignore discounts and onboarding if they are real.
### 4. Show payback only if retention is known

If retention is a guess, label payback as illustrative and do not lead with it.
### 5. Sensitivity

Name the one assumption that swings the answer. Recommend improving that input, not decorating the model.
### 6. Decision

Say whether the unit, on the user's numbers, funds its own acquisition and delivery. Do not invent a benchmark to declare victory.

## Output

Deliver a **unit economics sheet**.

- Purpose of this unit economics sheet, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs an unit economics sheet by 30 September 2026. A subscription team wants to know if a new annual plan clears contribution after onboarding labor.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A subscription team wants to know if a new annual plan clears contribution after onboarding labor.

The unit: customer, order, location, or contract: customer: in the file; order: not in the file; location: open; contract: in the file
Price and direct costs the user can support: CAD 49
Acquisition cost definition: CAD 18 direct. Overhead not in this line
Retention or repeat evidence, if any: one PDF, 2 pages, dated 14 September 2026
```

### Example outcome

**Unit economics sheet**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Defines the customer-year, keeps overhead out, and shows payback only to the extent retention evidence exists.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The unit: customer, order, location, or contract | customer: in the file; order: not in the file; location: open; contract: in the file | Needs confirmation |
| Price and direct costs the user can support | CAD 49 | Carried into the draft |
| Acquisition cost definition | CAD 18 direct. Overhead not in this line | Carried into the draft |
| Retention or repeat evidence, if any | one PDF, 2 pages, dated 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Define the unit**  
Say exactly what one unit is. Mixing orders and customers in one margin is how teams fool themselves.

**2. Build contribution**  
Price minus costs that vary with the unit. Keep fixed overhead out of the unit and show it separately.

**3. Treat acquisition honestly**  
Include the costs the user says are required to win the unit. Do not ignore discounts and onboarding if they are real.

**4. Show payback only if retention is known**  
If retention is a guess, label payback as illustrative and do not lead with it.

**5. Sensitivity**  
Name the one assumption that swings the answer. Recommend improving that input, not decorating the model.

**Deliberately not done**
- A lifetime value built on an invented retention curve.
- Forgetting discounts, refunds, or implementation cost.
- Comparing the result to a generic SaaS benchmark from memory.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A lifetime value built on an invented retention curve.
- Forgetting discounts, refunds, or implementation cost.
- Comparing the result to a generic SaaS benchmark from memory.

## Related skills

- `pricing-margin-bridge`
- `saas-metrics-pack`
- `break-even-analysis`
