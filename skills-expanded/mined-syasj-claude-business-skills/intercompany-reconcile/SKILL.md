---
name: intercompany-reconcile
description: "Reconcile balances and transactions between entities so the group is not adding numbers that do not eliminate. Use when the user mentions intercompany, intercompany reconciliation, elimination entries, related party balances, or asks for a intercompany reconciliation. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'intercompany-reconcile' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Intercompany Reconciliation

Reconcile balances and transactions between entities so the group is not adding numbers that do not eliminate.

## When to use this skill

Use this skill when the user:

- intercompany
- intercompany reconciliation
- elimination entries
- related party balances

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

- Entities involved
- Balances each side recorded
- In-transit items
- Who approves eliminations

## Workflow


### 1. Match both sides

Entity A receivable against entity B payable, same period. One-sided balances are the work.
### 2. Classify differences

In-transit cash, FX, timing of invoices, or a booking error. Use the user's currency facts. Do not invent rates.
### 3. Profit in inventory

If they sell goods between entities, flag unrealized profit as a question for their policy. Do not compute a tax position.
### 4. Draft the elimination

Show the eliminating lines as a proposal that references both sides.
### 5. Aging of differences

Old intercompany differences are a control failure, not a rounding issue.
### 6. Owner going forward

A monthly match, with a named preparer, beats an annual archaeology project.

## Output

Deliver a **intercompany reconciliation**.

- Purpose of this intercompany reconciliation, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an intercompany reconciliation by 30 September 2026. Two subsidiaries disagree by a material amount on a management fee, and the group close is tomorrow.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Two subsidiaries disagree by a material amount on a management fee, and the group close is tomorrow.

Entities involved: Undeposited funds. Stated in the ask, not documented anywhere else
Balances each side recorded: one file, dated 14 September 2026. No earlier version attached for comparison
In-transit items: Sales tax payable, last reviewed 14 September 2026. No owner named since
Who approves eliminations: Priya Shah, controller
```

### Example outcome

**Intercompany reconciliation**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Does not force a missing counterparty into existence.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Entities involved | Undeposited funds. Stated in the ask, not documented anywhere else | Needs confirmation |
| Balances each side recorded | one file, dated 14 September 2026. No earlier version attached for comparison | Carried into the draft |
| In-transit items | Sales tax payable, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Who approves eliminations | Priya Shah, controller | Needs confirmation |

**How this draft was built**

**1. Match both sides**  
Entity A receivable against entity B payable, same period. One-sided balances are the work.

**2. Classify differences**  
In-transit cash, FX, timing of invoices, or a booking error. Use the user's currency facts. Do not invent rates.

**3. Profit in inventory**  
If they sell goods between entities, flag unrealized profit as a question for their policy. Do not compute a tax position.

**4. Draft the elimination**  
Show the eliminating lines as a proposal that references both sides.

**5. Aging of differences**  
Old intercompany differences are a control failure, not a rounding issue.

**Deliberately not done**
- Eliminating a one-sided balance with no counterparty.
- Inventing an FX rate.
- Leaving multi-year differences as 'timing'.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Eliminating a one-sided balance with no counterparty.
- Inventing an FX rate.
- Leaving multi-year differences as 'timing'.

## Related skills

- `month-end-close`
- `journal-entry-review`
- `fx-exposure-review`
