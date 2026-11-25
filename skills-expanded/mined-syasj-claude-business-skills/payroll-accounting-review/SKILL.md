---
name: payroll-accounting-review
description: "Review the payroll journal path from the payroll register to the ledger, including accruals and remittances. Use when the user mentions payroll accounting, payroll journal, payroll accrual, wage reconciliation, or asks for a payroll accounting review. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'payroll-accounting-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Payroll Accounting Review

Review the payroll journal path from the payroll register to the ledger, including accruals and remittances.

## When to use this skill

Use this skill when the user:

- payroll accounting
- payroll journal
- payroll accrual
- wage reconciliation

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not an audit opinion, compilation, or tax advice. Do not invent accounting standards. Use the policy, framework, and chart of accounts the organization actually follows.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Payroll register totals
- Ledger accounts used
- Remittances due
- Known off-cycle payments

## Workflow


### 1. Tie the register to the journal

Gross pay, deductions, employer costs, and net pay. A difference is a finding, not a rounding story, unless they show the rounding.
### 2. Liability accounts

Deductions and employer taxes should land in liabilities until remitted. Net pay sitting in an expense account is a mapping question.
### 3. Accrual

Days worked but not paid at period end. Use their calendar. Do not invent a pay cycle.
### 4. Off-cycle and manual payments

List them and ask whether they hit the same controls.
### 5. Remittance calendar

What is due, without giving tax advice. The skill schedules their stated dues. It does not opine on tax law.
### 6. Access

Recommend that the person who changes pay rates is not the only person who reviews the register. Do not ask for payroll-system passwords.

## Output

Deliver a **payroll accounting review**.

- Purpose of this payroll accounting review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a payroll accounting review by 30 September 2026. The payroll register and the wage expense account have not matched for two months.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The payroll register and the wage expense account have not matched for two months.

Payroll register totals: CAD 70,000 on the 1st and the 15th
Ledger accounts used: 30 in the last period. No prior period attached, so no trend
Remittances due: Undeposited funds and one other, both unconfirmed as of 14 September 2026
Known off-cycle payments: Undeposited funds. Stated in the ask, not documented anywhere else
```

### Example outcome

**Payroll accounting review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A tie-out of gross-to-journal, a mapping question on liabilities, and a control note on who reviews the register.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Payroll register totals | CAD 70,000 on the 1st and the 15th | Needs confirmation |
| Ledger accounts used | 30 in the last period. No prior period attached, so no trend | Carried into the draft |
| Remittances due | Undeposited funds and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Known off-cycle payments | Undeposited funds. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Tie the register to the journal**  
Gross pay, deductions, employer costs, and net pay. A difference is a finding, not a rounding story, unless they show the rounding.

**2. Liability accounts**  
Deductions and employer taxes should land in liabilities until remitted. Net pay sitting in an expense account is a mapping question.

**3. Accrual**  
Days worked but not paid at period end. Use their calendar. Do not invent a pay cycle.

**4. Off-cycle and manual payments**  
List them and ask whether they hit the same controls.

**5. Remittance calendar**  
What is due, without giving tax advice. The skill schedules their stated dues. It does not opine on tax law.

**Deliberately not done**
- Inventing tax rates.
- Ignoring off-cycle payments.
- Asking for payroll logins.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Inventing tax rates.
- Ignoring off-cycle payments.
- Asking for payroll logins.

## Related skills

- `month-end-close`
- `accrual-policy`
- `internal-controls-walkthrough`
