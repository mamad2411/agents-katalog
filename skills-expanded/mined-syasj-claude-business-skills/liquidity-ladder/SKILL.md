---
name: liquidity-ladder
description: "Build a simple liquidity ladder from cash, committed inflows, and committed outflows. Use when the user mentions liquidity ladder, cash ladder, treasury forecast, short-term liquidity, or asks for a liquidity ladder. Banking and treasury operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: banking
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'liquidity-ladder' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Liquidity Ladder

Build a simple liquidity ladder from cash, committed inflows, and committed outflows.

## When to use this skill

Use this skill when the user:

- liquidity ladder
- cash ladder
- treasury forecast
- short-term liquidity

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

- Cash by account
- Committed inflows
- Committed outflows
- Available facilities they described

## Workflow


### 1. Step 1

Group by the buckets they care about, such as this week and this month.
### 2. Step 2

Include only committed items unless an uncommitted item is clearly labeled.
### 3. Step 3

Show facilities separately from cash.
### 4. Step 4

Flag the first bucket that fails their minimum.
### 5. Step 5

Do not move money or request credentials.
### 6. Step 6

Recommend a decision for the treasurer, not a trade.

## Output

Deliver a **liquidity ladder**.

- Purpose of this liquidity ladder, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a liquidity ladder by 30 September 2026. A ladder treats an undrawn line as money already in the account.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A ladder treats an undrawn line as money already in the account.

Cash by account: 30 in the last period. No prior period attached, so no trend
Committed inflows: the one named in the ask. Version and owner not recorded
Committed outflows: the one named in the ask. Version and owner not recorded
Available facilities they described: Account opening file 221. Stated in the ask, not documented anywhere else
```

### Example outcome

**Liquidity ladder**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Separates the line from cash and flags the first short bucket.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Cash by account | 30 in the last period. No prior period attached, so no trend | Needs confirmation |
| Committed inflows | the one named in the ask. Version and owner not recorded | Carried into the draft |
| Committed outflows | the one named in the ask. Version and owner not recorded | Carried into the draft |
| Available facilities they described | Account opening file 221. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Group by the buckets they care about, such as this week and this month**

**2. Include only committed items unless an uncommitted item is clearly labeled**

**3. Show facilities separately from cash**

**4. Flag the first bucket that fails their minimum**

**5. Do not move money or request credentials**

**Deliberately not done**
- A facility shown as cash.
- Uncommitted inflow shown as certain.
- A credential request.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A facility shown as cash
- Uncommitted inflow shown as certain
- A credential request

## Related skills

- `cash-flow-forecast`
- `treasury-policy-brief`
