---
name: cash-flow-forecast
description: "Build a 13-week direct cash forecast from collections and commitments, not from accrual revenue. Use when the user mentions 13-week cash, cash forecast, when do we run out of money, weekly cash, or asks for a 13-week cash forecast. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'cash-flow-forecast' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Cash Flow Forecast

Build a 13-week direct cash forecast from collections and commitments, not from accrual revenue.

## When to use this skill

Use this skill when the user:

- 13-week cash
- cash forecast
- when do we run out of money
- weekly cash
- liquidity forecast

## When not to use this skill

- Tax advice
- A promise of funding

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

- Opening cash by entity and currency
- Receivables and the user's collection experience
- Payroll, tax, rent, and debt dates
- Approved payables and known one-offs

## Workflow


### 1. Lock the frame

Use 13 weeks unless the user asked for another horizon. Record opening cash by account. Do not net cash against a credit line unless they treat that line as cash.
### 2. Forecast collections

Inflows come from expected cash collected, not from revenue booked. Use the user's lag. If they have no history, mark a stated assumption and keep it visible.
### 3. List commitments

Payroll, taxes, rent, debt service, and approved payables are committed. Discretionary spend sits in a separate row.
### 4. Show one-offs

Financing, capex, and owner transfers get their own lines. Do not bury them in operations.
### 5. Roll forward

Opening plus inflows minus outflows equals closing, every week. Flag any week under the user's minimum buffer.
### 6. Stress it

Slip collections by the delay the user fears, and pull one large payment forward. Name the first week that breaks. Do not call the forecast a guarantee.

## Output

Deliver a **13-week cash forecast**.

- Purpose of this 13-week cash forecast, in two sentences.
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

Mara Chen runs Northline Studio in Calgary. On 14 September 2026 she asks whether she can start two producers next month without missing payroll. She will not finish a week under 40,000 CAD. A customer owes 90,000 and usually pays 20 days late. That money is not in the bank.

### Example data

```text
opening cash: 180000 CAD, operating account, 14 Sep 2026, one entity
payroll: 70000 on the 1st and the 15th
rent: 12000 due in week 3
approved bills: 8400 due in week 2
receivable: Harbor & Co, 90000, usually 20 days late, not collected
buffer: do not finish a week under 40000
proposed hires: 2 producers, 8500 each per month, start week 5
credit line: exists, she does not treat it as cash
```

### Example outcome

**13-week cash view — first five weeks**
Northline Studio · 14 September 2026 · CAD

Decision: do not send the two offers on this file. Week 3 closes under the 40,000 buffer before Harbor & Co pays. The hire is a cash condition, not a yes.

| Week | Opening | In | Out | Closing | Vs 40,000 |
| --- | --- | --- | --- | --- | --- |
| 1 | 180,000 | 0 | 70,000 payroll | 110,000 | above |
| 2 | 110,000 | 0 | 8,400 bills | 101,600 | above |
| 3 | 101,600 | 0 | 82,000 payroll and rent | 19,600 | below |
| 4 | 19,600 | 90,000 if the 20-day lag holds | 0 | 109,600 | above |
| 5 | 109,600 | 0 | 70,000 payroll, hires not included | 39,600 | below |

The 90,000 is a collection, not revenue. It is placed in week 4 only because that is her lag.
The two hires are not in the table. Adding 8,500 each would make week 5 worse.
Not a guarantee. She confirms the Harbor date before any offer goes out.
Next: Mara, by 18 September.

## Anti-patterns

- Starting from an accrual P&L and calling it cash.
- Hiding a financing need inside 'other'.
- Presenting a single unstressed line as certainty.

## Related skills

- `runway-and-burn`
- `working-capital`
- `budget-variance-review`

## Optional local tool

A stdlib script is bundled at `scripts/cashflow_check.py`. It rolls a CSV of `week,inflow,outflow` forward from an opening balance you pass with `--opening`. It does not fetch bank data, rates, or credentials. Example: `python3 scripts/cashflow_check.py weeks.csv --opening 100000 --buffer 25000 --json`. For the assumption log format, see [references/assumptions.md](references/assumptions.md).
