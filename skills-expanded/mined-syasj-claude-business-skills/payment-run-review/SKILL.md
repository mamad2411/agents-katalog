---
name: payment-run-review
description: "Review a payment run for duplicates, approvals, and changes to payee details. Use when the user mentions payment run, AP run review, pay cycle review, payment approval, or asks for a payment run review. Banking and treasury operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: banking
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'payment-run-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Payment Run Review

Review a payment run for duplicates, approvals, and changes to payee details.

## When to use this skill

Use this skill when the user:

- payment run
- AP run review
- pay cycle review
- payment approval

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not a credit decision and not an instruction to move money. Do not request online-banking passwords, one-time codes, or card PINs.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The run list
- Approval limits
- Changed payee details
- Exceptions

## Workflow


### 1. Step 1

Check the run against approvals they require.
### 2. Step 2

Flag duplicate-looking items for review, not as accusations.
### 3. Step 3

Any payee detail change needs their verified channel.
### 4. Step 4

Do not ask for banking passwords or one-time codes.
### 5. Step 5

Exceptions need a named approver.
### 6. Step 6

Recommend a hold on items that fail the check rather than a silent release.

## Output

Deliver a **payment run review**.

- Purpose of this payment run review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a payment run review by 30 September 2026. A payment run includes a new account number received by email this morning.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A payment run includes a new account number received by email this morning.

The run list: Payment run 14 Sep; Account opening file 221; Liquidity ladder
Approval limits: Account opening file 221. Partly documented: the what is written down, the who is not
Changed payee details: requested 14 September 2026. Not yet approved
Exceptions: Payment run 14 Sep is open. Account opening file 221 was raised verbally and never logged
```

### Example outcome

**Payment run review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Holds that item until the verified channel confirms it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The run list | Payment run 14 Sep; Account opening file 221; Liquidity ladder | Needs confirmation |
| Approval limits | Account opening file 221. Partly documented: the what is written down, the who is not | Carried into the draft |
| Changed payee details | requested 14 September 2026. Not yet approved | Carried into the draft |
| Exceptions | Payment run 14 Sep is open. Account opening file 221 was raised verbally and never logged | Needs confirmation |

**How this draft was built**

**1. Check the run against approvals they require**

**2. Flag duplicate-looking items for review, not as accusations**

**3. Any payee detail change needs their verified channel**

**4. Do not ask for banking passwords or one-time codes**

**5. Exceptions need a named approver**

**Deliberately not done**
- A password request.
- A silent release of a failed item.
- An unverified bank-detail change.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A password request
- A silent release of a failed item
- An unverified bank-detail change

## Related skills

- `accounts-payable-control`
- `treasury-policy-brief`
