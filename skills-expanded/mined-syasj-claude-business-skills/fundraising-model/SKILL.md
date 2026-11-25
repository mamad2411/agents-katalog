---
name: fundraising-model
description: "Lay out how much cash a raise needs to buy, what it funds, and what remains unresolved. Not a valuation. Use when the user mentions fundraising model, use of proceeds, how much should we raise, runway raise, or asks for a fundraising use-of-proceeds model. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'fundraising-model' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Fundraising Model

Lay out how much cash a raise needs to buy, what it funds, and what remains unresolved. Not a valuation.

## When to use this skill

Use this skill when the user:

- fundraising model
- use of proceeds
- how much should we raise
- runway raise

## When not to use this skill

- Investment advice
- Inventing investor demand

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

- Current cash and monthly burn the user stands behind
- The plan the raise is meant to fund
- Target months of runway
- Known financing terms, if any

## Workflow


### 1. Start from the plan

The raise follows the operating plan, not the other way around. If there is no plan, say the amount cannot be justified yet.
### 2. Build a monthly cash view

Use the user's costs. Separate hiring that is required for the plan from hiring that is optional.
### 3. Add a buffer

Recommend a stated buffer for timing slips. Call it a buffer, not a pretend precision.
### 4. Use of proceeds

Group the money into a few uses a investor or lender can audit later. No 'miscellaneous growth' bucket over a small share unless the user insists, and then flag it.
### 5. Do not value the company

If the user supplies a price, you may show dilution math as arithmetic. Do not invent a valuation.
### 6. State what the money will not do

The milestones this raise does not buy. Overclaiming the plan is how raises become stories.

## Output

Deliver a **fundraising use-of-proceeds model**.

- Purpose of this fundraising use-of-proceeds model, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a fundraising use-of-proceeds model by 30 September 2026. A founder wants to raise '18 months of runway' and has a hiring plan that is not in the current burn.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A founder wants to raise '18 months of runway' and has a hiring plan that is not in the current burn.

Current cash and monthly burn the user stands behind: Harbor & Co receipt and one other, both unconfirmed as of 14 September 2026
The plan the raise is meant to fund: Operating cash, recorded 14 September 2026. No supporting file attached
Target months of runway: 160
Known financing terms, if any: Harbor & Co receipt. Stated in the ask, not documented anywhere else
```

### Example outcome

**Fundraising use-of-proceeds model**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A monthly cash view, a recommended buffer, a use-of-proceeds grouping, and an explicit statement that valuation is outside this skill.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Current cash and monthly burn the user stands behind | Harbor & Co receipt and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |
| The plan the raise is meant to fund | Operating cash, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Target months of runway | 160 | Carried into the draft |
| Known financing terms, if any | Harbor & Co receipt. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Start from the plan**  
The raise follows the operating plan, not the other way around. If there is no plan, say the amount cannot be justified yet.

**2. Build a monthly cash view**  
Use the user's costs. Separate hiring that is required for the plan from hiring that is optional.

**3. Add a buffer**  
Recommend a stated buffer for timing slips. Call it a buffer, not a pretend precision.

**4. Use of proceeds**  
Group the money into a few uses a investor or lender can audit later. No 'miscellaneous growth' bucket over a small share unless the user insists, and then flag it.

**5. Do not value the company**  
If the user supplies a price, you may show dilution math as arithmetic. Do not invent a valuation.

**Deliberately not done**
- Choosing a raise amount because it sounds normal.
- Inventing a pre-money valuation.
- A use-of-proceeds slide that does not tie to the cash model.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Choosing a raise amount because it sounds normal.
- Inventing a pre-money valuation.
- A use-of-proceeds slide that does not tie to the cash model.

## Related skills

- `runway-and-burn`
- `investment-memo`
- `cash-flow-forecast`
