---
name: accrual-policy
description: "Draft a short accrual policy so estimates are consistent, documented, and reversed on purpose. Use when the user mentions accrual policy, when do we accrue, month-end accruals, estimate policy, or asks for a accrual policy draft. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'accrual-policy' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Accrual Policy

Draft a short accrual policy so estimates are consistent, documented, and reversed on purpose.

## When to use this skill

Use this skill when the user:

- accrual policy
- when do we accrue
- month-end accruals
- estimate policy

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

- Types of accruals they actually book
- Materiality
- Who approves estimates
- Reversal practice today

## Workflow


### 1. List the real accruals

Payroll, bonuses, received-not-invoiced, and others they named. Do not add a textbook list they do not use.
### 2. Set the threshold

Below materiality, a practical rule beats false precision. Use their number or propose one as a draft.
### 3. Evidence

Each accrual names its source document or calculation. 'Management believes' is not a method.
### 4. Reversals

State whether the accrual reverses next period automatically and who checks the reversal did not double-count an invoice.
### 5. Changes in estimate

How a changed assumption is noted. Do not hide a target-driven change.
### 6. Owner

The policy names the approver. This draft is not itself a policy until they adopt it.

## Output

Deliver a **accrual policy draft**.

- Purpose of this accrual policy draft, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an accrual policy draft by 30 September 2026. Bonus accruals are booked differently by two entities, and neither documents the driver.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Bonus accruals are booked differently by two entities, and neither documents the driver.

Types of accruals they actually book: Undeposited funds. Partly documented: the what is written down, the who is not
Materiality: Undeposited funds, recorded 14 September 2026. No supporting file attached
Who approves estimates: Priya Shah, controller
Reversal practice today: Operating cash and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Accrual policy draft**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A short draft policy covering their actual accruals, evidence, reversal, and an approver, marked as a draft.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Types of accruals they actually book | Undeposited funds. Partly documented: the what is written down, the who is not | Needs confirmation |
| Materiality | Undeposited funds, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Who approves estimates | Priya Shah, controller | Carried into the draft |
| Reversal practice today | Operating cash and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. List the real accruals**  
Payroll, bonuses, received-not-invoiced, and others they named. Do not add a textbook list they do not use.

**2. Set the threshold**  
Below materiality, a practical rule beats false precision. Use their number or propose one as a draft.

**3. Evidence**  
Each accrual names its source document or calculation. 'Management believes' is not a method.

**4. Reversals**  
State whether the accrual reverses next period automatically and who checks the reversal did not double-count an invoice.

**5. Changes in estimate**  
How a changed assumption is noted. Do not hide a target-driven change.

**Deliberately not done**
- A policy copied from a large public company.
- Accruals with no evidence standard.
- Target-driven estimates treated as normal.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A policy copied from a large public company.
- Accruals with no evidence standard.
- Target-driven estimates treated as normal.

## Related skills

- `journal-entry-review`
- `month-end-close`
- `management-accounting-pack`
