---
name: account-reconciliation-standard
description: "Set a standard for balance-sheet reconciliations: purpose, frequency, evidence, and aging of open items. Use when the user mentions reconciliation standard, balance sheet reconciliations, rec policy, account ownership, or asks for a reconciliation standard. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'account-reconciliation-standard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Account Reconciliation Standard

Set a standard for balance-sheet reconciliations: purpose, frequency, evidence, and aging of open items.

## When to use this skill

Use this skill when the user:

- reconciliation standard
- balance sheet reconciliations
- rec policy
- account ownership

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

- Material balance-sheet accounts
- Current reconcilers
- How old open items get
- Reviewer

## Workflow


### 1. Assign every material account

An account without an owner is unreconciled even if the balance looks quiet.
### 2. Define a proper recon

Source, book balance, itemized difference, and age of each open item.
### 3. Frequency

Cash monthly at minimum, other accounts on a risk basis they agree. Do not demand a daily recon of every accrual without a reason.
### 4. Aging policy

Open items older than their threshold need a disposition plan, not a permanent home.
### 5. Review

Preparer and reviewer are different people for material accounts.
### 6. Storage

Where the evidence lives. Not in a personal inbox only, and not behind a shared password.

## Output

Deliver a **reconciliation standard**.

- Purpose of this reconciliation standard, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a reconciliation standard by 30 September 2026. Several balance-sheet accounts have no named preparer, and cash recs live in one person's inbox.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Several balance-sheet accounts have no named preparer, and cash recs live in one person's inbox.

Material balance-sheet accounts: one file, dated 14 September 2026. No earlier version attached for comparison
Current reconcilers: Undeposited funds and one other, both unconfirmed as of 14 September 2026
How old open items get: Undeposited funds, last reviewed 14 September 2026. No owner named since
Reviewer: Priya Shah. No second reviewer named
```

### Example outcome

**Reconciliation standard**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Assigns owners, defines a proper recon, and moves evidence to a shared location without shared passwords.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Material balance-sheet accounts | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| Current reconcilers | Undeposited funds and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| How old open items get | Undeposited funds, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Reviewer | Priya Shah. No second reviewer named | Needs confirmation |

**How this draft was built**

**1. Assign every material account**  
An account without an owner is unreconciled even if the balance looks quiet.

**2. Define a proper recon**  
Source, book balance, itemized difference, and age of each open item.

**3. Frequency**  
Cash monthly at minimum, other accounts on a risk basis they agree. Do not demand a daily recon of every accrual without a reason.

**4. Aging policy**  
Open items older than their threshold need a disposition plan, not a permanent home.

**5. Review**  
Preparer and reviewer are different people for material accounts.

**Deliberately not done**
- A policy that says 'reconcile everything daily'.
- Open items older than a year with no comment.
- Shared logins to the evidence folder.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A policy that says 'reconcile everything daily'.
- Open items older than a year with no comment.
- Shared logins to the evidence folder.

## Related skills

- `bank-reconciliation`
- `month-end-close`
- `internal-controls-walkthrough`
