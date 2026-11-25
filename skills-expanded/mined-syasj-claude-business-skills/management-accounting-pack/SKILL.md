---
name: management-accounting-pack
description: "Turn the ledger into a decision view: margins, cost centers, and a reconciliation back to the books. Use when the user mentions management accounts, cost center reporting, margin by line, internal financials, or asks for a management accounting pack. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'management-accounting-pack' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Management Accounting Pack

Turn the ledger into a decision view: margins, cost centers, and a reconciliation back to the books.

## When to use this skill

Use this skill when the user:

- management accounts
- cost center reporting
- margin by line
- internal financials

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

- Ledger for the period
- Dimensions they have: team, product, location
- Allocations they currently use
- The decision the pack serves

## Workflow


### 1. Reconcile to the ledger

Every management view ties to the GL in a bridge. Untied 'adjusted' numbers are labeled non-GAAP or internal, in their words, and still bridge.
### 2. Choose the cut

Product, location, or customer. One primary cut. A second cut only if they use it to decide.
### 3. Allocations

Describe the driver they use. If there is no driver, show the cost as unallocated rather than inventing a spread.
### 4. Contribution before overhead

Show a view before allocations so managers can see what they influence.
### 5. Commentary

Three movements that matter, with facts. No invented market color.
### 6. Owner

Who refreshes the pack after close, and on which day.

## Output

Deliver a **management accounting pack**.

- Purpose of this management accounting pack, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a management accounting pack by 30 September 2026. Leaders want margin by service line, but half of delivery cost sits in a general pool.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Leaders want margin by service line, but half of delivery cost sits in a general pool.

Ledger for the period: month ending 14 September 2026
Dimensions they have: team, product, location: team: in the file; product: not in the file; location: open
Allocations they currently use: Sales tax payable and one other, both unconfirmed as of 14 September 2026
The decision the pack serves: Leaders want margin by service line, but half of delivery cost sits in a general pool
```

### Example outcome

**Management accounting pack**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows contribution before allocation, labels the pool as unallocated, and bridges to the ledger.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Ledger for the period | month ending 14 September 2026 | Needs confirmation |
| Dimensions they have: team, product, location | team: in the file; product: not in the file; location: open | Carried into the draft |
| Allocations they currently use | Sales tax payable and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| The decision the pack serves | Leaders want margin by service line, but half of delivery cost sits in a general pool | Needs confirmation |

**How this draft was built**

**1. Reconcile to the ledger**  
Every management view ties to the GL in a bridge. Untied 'adjusted' numbers are labeled non-GAAP or internal, in their words, and still bridge.

**2. Choose the cut**  
Product, location, or customer. One primary cut. A second cut only if they use it to decide.

**3. Allocations**  
Describe the driver they use. If there is no driver, show the cost as unallocated rather than inventing a spread.

**4. Contribution before overhead**  
Show a view before allocations so managers can see what they influence.

**5. Commentary**  
Three movements that matter, with facts. No invented market color.

**Deliberately not done**
- A management P&L that does not bridge to the books.
- Allocations with a made-up driver.
- Ten cuts and no decision.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A management P&L that does not bridge to the books.
- Allocations with a made-up driver.
- Ten cuts and no decision.

## Related skills

- `chart-of-accounts-design`
- `kpi-tree-finance`
- `budget-variance-review`
