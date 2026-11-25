---
name: month-end-close
description: "Run a practical month-end close that produces one set of numbers and a short list of judgments. Use when the user mentions month-end close, close the books, close calendar, soft close, or asks for a month-end close pack. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'month-end-close' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Month-End Close

Run a practical month-end close that produces one set of numbers and a short list of judgments.

## When to use this skill

Use this skill when the user:

- month-end close
- close the books
- close calendar
- soft close

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

- Period and entities
- Open reconciliations
- Known judgments
- Sign-off owner

## Workflow


### 1. Freeze the checklist

Use their close list. Add a missing reconciliation only if a balance sheet account has no owner.
### 2. Clear suspense

Items in suspense need a destination or a labeled open item. Do not leave a plug and call the period closed.
### 3. Record judgments

Accruals, cut-off, and estimates get a note with the fact pattern and the person who accepted it.
### 4. Flux before sign-off

Explain material movements in plain language. A journal without a flux story is not reviewed.
### 5. Lock and list

After sign-off, list post-close entries separately. Quiet edits are how trust dies.
### 6. Hand the pack to reporting

Close produces numbers. The management pack explains them. Do not mix the two jobs in one heroic afternoon if both are slipping.

## Output

Deliver a **month-end close pack**.

- Purpose of this month-end close pack, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a month-end close pack by 30 September 2026. The controller wants a soft close by day six and cash is still unreconciled on day five.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The controller wants a soft close by day six and cash is still unreconciled on day five.

Period and entities: month ending 14 September 2026
Open reconciliations: Operating cash and one other, both unconfirmed as of 14 September 2026
Known judgments: Undeposited funds. Stated in the ask, not documented anywhere else
Sign-off owner: Priya Shah, controller
```

### Example outcome

**Month-end close pack**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses sign-off on unreconciled cash, lists open judgments, and separates any late entries.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Period and entities | month ending 14 September 2026 | Needs confirmation |
| Open reconciliations | Operating cash and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Known judgments | Undeposited funds. Stated in the ask, not documented anywhere else | Carried into the draft |
| Sign-off owner | Priya Shah, controller | Needs confirmation |

**How this draft was built**

**1. Freeze the checklist**  
Use their close list. Add a missing reconciliation only if a balance sheet account has no owner.

**2. Clear suspense**  
Items in suspense need a destination or a labeled open item. Do not leave a plug and call the period closed.

**3. Record judgments**  
Accruals, cut-off, and estimates get a note with the fact pattern and the person who accepted it.

**4. Flux before sign-off**  
Explain material movements in plain language. A journal without a flux story is not reviewed.

**5. Lock and list**  
After sign-off, list post-close entries separately. Quiet edits are how trust dies.

**Deliberately not done**
- Closing with an unreconciled cash account.
- Post-close journals with no log.
- A narrative that invents reasons for a variance.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Closing with an unreconciled cash account.
- Post-close journals with no log.
- A narrative that invents reasons for a variance.

## Related skills

- `financial-close-checklist`
- `bank-reconciliation`
- `journal-entry-review`
