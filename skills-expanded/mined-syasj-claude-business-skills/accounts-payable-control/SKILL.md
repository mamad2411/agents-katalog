---
name: accounts-payable-control
description: "Tighten payables so the company pays the right vendor, once, with evidence. Use when the user mentions accounts payable, duplicate payment, AP control, vendor payments, or asks for a payables control review. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'accounts-payable-control' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Accounts Payable Control

Tighten payables so the company pays the right vendor, once, with evidence.

## When to use this skill

Use this skill when the user:

- accounts payable
- duplicate payment
- AP control
- vendor payments

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

- How invoices arrive
- Who can add a vendor
- Approval limits
- Recent duplicate or fraud scares, if any

## Workflow


### 1. Map the path

Invoice, receipt of goods or services, approval, payment. Note where one person can do two of those steps.
### 2. Vendor master

New vendors need evidence the user already requires, plus a second look. Do not ask for or store bank passwords. Do not invent a vendor's bank details.
### 3. Three-way match where it fits

Purchase, receipt, and invoice. Where a match does not fit, say what alternative evidence they use.
### 4. Duplicate test

Same vendor, similar amount, close dates. Recommend a review list, not an automatic accusation.
### 5. Payment run

Who reviews the run before release, and how exceptions are logged.
### 6. Keep evidence

What is retained and for how long, using their retention rule if they have one. Do not invent a legal retention period.

## Output

Deliver a **payables control review**.

- Purpose of this payables control review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a payables control review by 30 September 2026. Two similar invoices from the same supplier were paid last quarter.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Two similar invoices from the same supplier were paid last quarter.

How invoices arrive: plain, for people who already know the context. No house guide attached
Who can add a vendor: Priya Shah, controller
Approval limits: Undeposited funds. Partly documented: the what is written down, the who is not
Recent duplicate or fraud scares, if any: Sales tax payable. Partly documented: the what is written down, the who is not
```

### Example outcome

**Payables control review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Separates vendor setup from payment release and proposes a duplicate review list without accusing the supplier.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| How invoices arrive | plain, for people who already know the context. No house guide attached | Needs confirmation |
| Who can add a vendor | Priya Shah, controller | Carried into the draft |
| Approval limits | Undeposited funds. Partly documented: the what is written down, the who is not | Carried into the draft |
| Recent duplicate or fraud scares, if any | Sales tax payable. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Map the path**  
Invoice, receipt of goods or services, approval, payment. Note where one person can do two of those steps.

**2. Vendor master**  
New vendors need evidence the user already requires, plus a second look. Do not ask for or store bank passwords. Do not invent a vendor's bank details.

**3. Three-way match where it fits**  
Purchase, receipt, and invoice. Where a match does not fit, say what alternative evidence they use.

**4. Duplicate test**  
Same vendor, similar amount, close dates. Recommend a review list, not an automatic accusation.

**5. Payment run**  
Who reviews the run before release, and how exceptions are logged.

**Deliberately not done**
- One person adds vendors and releases payments with no second look.
- Calling every duplicate-looking item fraud.
- Requesting banking passwords.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- One person adds vendors and releases payments with no second look.
- Calling every duplicate-looking item fraud.
- Requesting banking passwords.

## Related skills

- `expense-policy`
- `internal-controls-walkthrough`
- `vendor-contract-playbook`
