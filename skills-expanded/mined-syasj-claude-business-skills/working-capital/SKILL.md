---
name: working-capital
description: "Find cash trapped in receivables, inventory, or payables, and separate a process fix from a one-time release. Use when the user mentions working capital, cash conversion, DSO DIO DPO, cash trapped in the balance sheet, or asks for a working-capital review. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'working-capital' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Working Capital Review

Find cash trapped in receivables, inventory, or payables, and separate a process fix from a one-time release.

## When to use this skill

Use this skill when the user:

- working capital
- cash conversion
- DSO DIO DPO
- cash trapped in the balance sheet

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

- Receivables, inventory, and payables balances
- Related revenue or cost, so days can be calculated
- Known disputes or obsolete stock
- Payment terms the user actually offers

## Workflow


### 1. Compute days only if the bases exist

Do not invent DSO. Show the formula you used.
### 2. Separate structural from overdue

Terms the company chose are not the same as customers paying late.
### 3. Look at concentration

A few old invoices or SKUs often hold the cash. Ask for the aging if it was not provided, and do not pretend you saw it.
### 4. Recommend a release that is real

Collections on disputed invoices are not a plan. Name what must be resolved first.
### 5. Watch the rebound

A one-time collection is not a new run-rate. Say whether the improvement persists.
### 6. Avoid squeezing suppliers blindly

Extending payables has a relationship and supply cost. State it.

## Output

Deliver a **working-capital review**.

- Purpose of this working-capital review, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a working-capital review by 30 September 2026. Cash is tight even though the company is profitable, and receivables grew faster than sales.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Cash is tight even though the company is profitable, and receivables grew faster than sales.

Receivables, inventory, and payables balances: Harbor & Co owes CAD 60,000, usually 20 days late
Related revenue or cost, so days can be calculated: CAD 36 direct. Overhead not in this line
Known disputes or obsolete stock: Harbor & Co receipt. Stated in the ask, not documented anywhere else
Payment terms the user actually offers: CAD 180, dates not set, cap not set
```

### Example outcome

**Working-capital review**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Calculates days from the user's bases, flags concentration if known, and separates a one-time release from a process change.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Receivables, inventory, and payables balances | Harbor & Co owes CAD 60,000, usually 20 days late | Needs confirmation |
| Related revenue or cost, so days can be calculated | CAD 36 direct. Overhead not in this line | Carried into the draft |
| Known disputes or obsolete stock | Harbor & Co receipt. Stated in the ask, not documented anywhere else | Carried into the draft |
| Payment terms the user actually offers | CAD 180, dates not set, cap not set | Needs confirmation |

**How this draft was built**

**1. Compute days only if the bases exist**  
Do not invent DSO. Show the formula you used.

**2. Separate structural from overdue**  
Terms the company chose are not the same as customers paying late.

**3. Look at concentration**  
A few old invoices or SKUs often hold the cash. Ask for the aging if it was not provided, and do not pretend you saw it.

**4. Recommend a release that is real**  
Collections on disputed invoices are not a plan. Name what must be resolved first.

**5. Watch the rebound**  
A one-time collection is not a new run-rate. Say whether the improvement persists.

**Deliberately not done**
- A days metric with no formula.
- Counting disputed receivables as cash you will collect next week.
- A supplier stretch with no service risk.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A days metric with no formula.
- Counting disputed receivables as cash you will collect next week.
- A supplier stretch with no service risk.

## Related skills

- `cash-flow-forecast`
- `accounts-receivable-control`
- `inventory-policy`
