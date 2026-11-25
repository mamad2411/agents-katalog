---
name: accounts-receivable-control
description: "Review receivables so the aging means something and cash collection is a process, not a hope. Use when the user mentions accounts receivable, AR aging, collections control, unapplied cash, or asks for a receivables control review. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'accounts-receivable-control' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Accounts Receivable Control

Review receivables so the aging means something and cash collection is a process, not a hope.

## When to use this skill

Use this skill when the user:

- accounts receivable
- AR aging
- collections control
- unapplied cash

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

- Aging by customer
- Billing terms
- Unapplied cash
- Disputes the user knows about

## Workflow


### 1. Tie the aging to the ledger

If the aging and the GL disagree, that is the first finding. Do not analyze a report that does not tie.
### 2. Split the buckets

Current, overdue, disputed, and unapplied. A disputed invoice is not a collections script.
### 3. Credit notes and cash application

Unapplied cash hides both problems and comfort. List it.
### 4. Concentration

A few customers may dominate overdue. Name them only from the user's data.
### 5. Write the action by bucket

Bill, call, resolve dispute, or reserve. Reserving is an accounting judgment for the policy owner, not a collection tactic.
### 6. Do not harass

Draft a factual collections note if asked. No threats, no shame language, no fake legal deadlines.

## Output

Deliver a **receivables control review**.

- Purpose of this receivables control review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a receivables control review by 30 September 2026. The AR aging shows a large over-90 bucket, and cash sits unapplied in the same report.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The AR aging shows a large over-90 bucket, and cash sits unapplied in the same report.

Aging by customer: Kite Freight
Billing terms: Operating cash and one other, both unconfirmed as of 14 September 2026
Unapplied cash: Sales tax payable, last reviewed 14 September 2026. No owner named since
Disputes the user knows about: Undeposited funds. Stated in the ask, not documented anywhere else
```

### Example outcome

**Receivables control review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Reconciles the aging, separates disputes from overdue, and lists unapplied cash before anyone writes a chase note.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Aging by customer | Kite Freight | Needs confirmation |
| Billing terms | Operating cash and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Unapplied cash | Sales tax payable, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Disputes the user knows about | Undeposited funds. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Tie the aging to the ledger**  
If the aging and the GL disagree, that is the first finding. Do not analyze a report that does not tie.

**2. Split the buckets**  
Current, overdue, disputed, and unapplied. A disputed invoice is not a collections script.

**3. Credit notes and cash application**  
Unapplied cash hides both problems and comfort. List it.

**4. Concentration**  
A few customers may dominate overdue. Name them only from the user's data.

**5. Write the action by bucket**  
Bill, call, resolve dispute, or reserve. Reserving is an accounting judgment for the policy owner, not a collection tactic.

**Deliberately not done**
- An aging that does not tie to the ledger.
- Treating disputes as lazy customers.
- Threatening language in a collections note.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An aging that does not tie to the ledger.
- Treating disputes as lazy customers.
- Threatening language in a collections note.

## Related skills

- `working-capital`
- `revenue-recognition-review`
- `bank-reconciliation`
