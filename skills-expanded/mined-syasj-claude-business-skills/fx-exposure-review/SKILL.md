---
name: fx-exposure-review
description: "Identify where currency actually hits cash, and separate a hedge policy question from a bookkeeping curiosity. Use when the user mentions FX exposure, currency risk, hedging review, exchange rate impact, or asks for a FX exposure review. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'fx-exposure-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Foreign Exchange Exposure Review

Identify where currency actually hits cash, and separate a hedge policy question from a bookkeeping curiosity.

## When to use this skill

Use this skill when the user:

- FX exposure
- currency risk
- hedging review
- exchange rate impact

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

- Currencies of revenue, costs, and cash
- Which exposures are contractual
- The user's hedge policy, if any
- The decision they need to make

## Workflow


### 1. Map cash exposures

Where currency hits a bank account, not only where a report is translated.
### 2. Separate transaction from translation

Management action usually belongs on contracted cash flows. Say which one the user is looking at.
### 3. Quantify only with their data

A rate move they specify, applied to exposures they listed. Do not invent a forecast rate and call it the market.
### 4. Policy before trades

If they have no hedge policy, recommend writing the policy questions, not a trade ticket.
### 5. Note operational natural hedges

Costs in the same currency as revenue may already offset. Do not propose a hedge that doubles the risk.
### 6. Hand off execution

This skill does not place trades or ask for brokerage logins.

## Output

Deliver a **FX exposure review**.

- Purpose of this FX exposure review, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a FX exposure review by 30 September 2026. A firm invoices in euros and pays staff in dollars and wants to know if last month's margin drop was FX.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A firm invoices in euros and pays staff in dollars and wants to know if last month's margin drop was FX.

Currencies of revenue, costs, and cash: CAD 44 direct. Overhead not in this line
Which exposures are contractual: unsigned draft, 8 pages, no signature date
The user's hedge policy, if any: their one-page rule dated 2 Mar 2026. No exception log
The decision they need to make: A firm invoices in euros and pays staff in dollars and wants to know if last month's margin drop was FX
```

### Example outcome

**Fx exposure review**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A map of contractual cash exposure, a translation-versus-transaction split, and policy questions rather than a trade order.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Currencies of revenue, costs, and cash | CAD 44 direct. Overhead not in this line | Needs confirmation |
| Which exposures are contractual | unsigned draft, 8 pages, no signature date | Carried into the draft |
| The user's hedge policy, if any | their one-page rule dated 2 Mar 2026. No exception log | Carried into the draft |
| The decision they need to make | A firm invoices in euros and pays staff in dollars and wants to know if last month's margin drop was FX | Needs confirmation |

**How this draft was built**

**1. Map cash exposures**  
Where currency hits a bank account, not only where a report is translated.

**2. Separate transaction from translation**  
Management action usually belongs on contracted cash flows. Say which one the user is looking at.

**3. Quantify only with their data**  
A rate move they specify, applied to exposures they listed. Do not invent a forecast rate and call it the market.

**4. Policy before trades**  
If they have no hedge policy, recommend writing the policy questions, not a trade ticket.

**5. Note operational natural hedges**  
Costs in the same currency as revenue may already offset. Do not propose a hedge that doubles the risk.

**Deliberately not done**
- Treating accounting translation as cash risk without checking.
- Inventing a hedge product and telling them to buy it.
- Asking for trading credentials.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Treating accounting translation as cash risk without checking.
- Inventing a hedge product and telling them to buy it.
- Asking for trading credentials.

## Related skills

- `pricing-margin-bridge`
- `cash-flow-forecast`
- `treasury-policy-brief`
