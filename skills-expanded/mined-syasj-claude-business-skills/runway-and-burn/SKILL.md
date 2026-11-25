---
name: runway-and-burn
description: "Compute cash runway from a defined burn, and show how hiring or a slipped receipt changes the date. Use when the user mentions runway, burn rate, how long is our cash, cash out date, or asks for a runway note. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'runway-and-burn' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Runway and Burn

Compute cash runway from a defined burn, and show how hiring or a slipped receipt changes the date.

## When to use this skill

Use this skill when the user:

- runway
- burn rate
- how long is our cash
- cash out date

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

- Cash on hand
- Which expenses are in burn
- Expected receipts the user wants included or excluded
- Upcoming committed hires

## Workflow


### 1. Define burn

State whether burn is cash operating burn, and whether financing or one-offs are excluded. Write the definition before the number.
### 2. Use a recent window

Prefer the user's last complete months over a single unusual week. Note if a month was distorted.
### 3. Compute the date

Cash divided by the defined monthly burn, then adjust for known receipts if the user wants a receipt-inclusive view. Show both if they differ.
### 4. Add the hire

Show the runway date with and without the committed hire. Do not hide the effect.
### 5. Name the lever

The one change that moves the date most, based on their numbers.
### 6. Avoid false comfort

A credit line is not cash unless they describe it as available and unconditional.

## Output

Deliver a **runway note**.

- Purpose of this runway note, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a runway note by 30 September 2026. A CEO says runway is 14 months, but the figure excludes two signed offers starting next month.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A CEO says runway is 14 months, but the figure excludes two signed offers starting next month.

Cash on hand: CAD 200,000 counted 14 September 2026
Which expenses are in burn: Payroll 15 September. Stated in the ask, not documented anywhere else
Expected receipts the user wants included or excluded: Operating cash and one other, both unconfirmed as of 14 September 2026
Upcoming committed hires: Payroll 15 September and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**13-week cash view, first four weeks shown**
Northline Studio · 14 September 2026 · CAD

Decision: do not add a new recurring cost until Kite Freight's 130,000 is collected or moved out of the plan. The hire is a cash condition, not a yes.

| Week | Opening | In | Out | Closing | Against buffer 25,000 |
| --- | --- | --- | --- | --- | --- |
| 1 | 200,000 | 0 | 60,000 payroll | 140,000 | above |
| 2 | 140,000 | 0 | 8,400 approved bills | 131,600 | above |
| 3 | 131,600 | 0 | 76,000 payroll and rent | 55,600 | above |
| 4 | 55,600 | 130,000 if the lag holds | 0 | 185,600 | above |

First tight week: none in the first four weeks.
Assumption: the 130,000 is collected in week 4 because that is the 20-day lag in the file. It is not booked revenue.
Not in this draft: a second scenario where the receipt slips past week 6. Build that before any offer letter.
Next action: Mara Chen confirms the collection date by 30 September 2026.

## Anti-patterns

- One runway number with no definition.
- Treating a facility as cash without the user's confirmation.
- Ignoring a hire that is already committed.

## Related skills

- `cash-flow-forecast`
- `fundraising-model`
- `workforce-plan`
