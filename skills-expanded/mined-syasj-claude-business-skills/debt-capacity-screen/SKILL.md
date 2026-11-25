---
name: debt-capacity-screen
description: "Screen whether a borrowing idea fits the user's cash generation, without acting as a lender. Use when the user mentions can we borrow, debt capacity, loan versus equity, covenant headroom, or asks for a debt capacity screen. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'debt-capacity-screen' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Debt Capacity Screen

Screen whether a borrowing idea fits the user's cash generation, without acting as a lender.

## When to use this skill

Use this skill when the user:

- can we borrow
- debt capacity
- loan versus equity
- covenant headroom

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

- Historical and expected cash generation the user provided
- Existing debt and covenants if known
- The use of the new money
- Security or guarantee constraints

## Workflow


### 1. State the use

Borrowing for a defined need is different from borrowing because it is available. If the use is vague, say so.
### 2. Look at coverage with their numbers

Show cash after maintenance needs versus proposed debt service. Do not invent a bank's credit box.
### 3. Include existing promises

Covenants and liens the user already has come first. If unknown, the screen is incomplete.
### 4. Compare with equity or delay

A screen that only cheers for debt is incomplete.
### 5. Name the questions a lender will ask

Evidence, not a predicted approval.
### 6. Do not request banking passwords or move money

This is a paper screen.

## Output

Deliver a **debt capacity screen**.

- Purpose of this debt capacity screen, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a debt capacity screen by 30 September 2026. A company wants a term loan to fund a fit-out and has an existing facility with covenants they only partly remember.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A company wants a term loan to fund a fit-out and has an existing facility with covenants they only partly remember.

Historical and expected cash generation the user provided: Operating cash. Partly documented: the what is written down, the who is not
Existing debt and covenants if known: Harbor & Co receipt, last reviewed 14 September 2026. No owner named since
The use of the new money: Operating cash, recorded 14 September 2026. No supporting file attached
Security or guarantee constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Debt capacity screen**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows service versus their cash, flags the missing covenant facts, and does not predict an approval.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Historical and expected cash generation the user provided | Operating cash. Partly documented: the what is written down, the who is not | Needs confirmation |
| Existing debt and covenants if known | Harbor & Co receipt, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The use of the new money | Operating cash, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Security or guarantee constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. State the use**  
Borrowing for a defined need is different from borrowing because it is available. If the use is vague, say so.

**2. Look at coverage with their numbers**  
Show cash after maintenance needs versus proposed debt service. Do not invent a bank's credit box.

**3. Include existing promises**  
Covenants and liens the user already has come first. If unknown, the screen is incomplete.

**4. Compare with equity or delay**  
A screen that only cheers for debt is incomplete.

**5. Name the questions a lender will ask**  
Evidence, not a predicted approval.

**Deliberately not done**
- Promising that a bank will say yes.
- Ignoring existing covenants because they were not in the teaser.
- A debt recommendation for an undefined use.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Promising that a bank will say yes.
- Ignoring existing covenants because they were not in the teaser.
- A debt recommendation for an undefined use.

## Related skills

- `fundraising-model`
- `capex-business-case`
- `cash-flow-forecast`
