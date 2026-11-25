---
name: three-statement-model
description: "Sketch how profit, cash, and the balance sheet stay tied together, at the level the user can actually support. Use when the user mentions three statement model, integrated forecast, P&L balance sheet cash flow, financial model structure, or asks for a linked three-statement sketch. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'three-statement-model' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Three-Statement Model

Sketch how profit, cash, and the balance sheet stay tied together, at the level the user can actually support.

## When to use this skill

Use this skill when the user:

- three statement model
- integrated forecast
- P&L balance sheet cash flow
- financial model structure

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

- Historical statements or the fact that they are unavailable
- Forecast horizon
- Debt, capex, and working-capital drivers
- What decision the model must support

## Workflow


### 1. Start from the decision

Build only the detail that decision needs. A full monthly model is not automatically better.
### 2. Link the statements

Net income flows to retained earnings. Depreciation, working capital, capex, and debt explain why profit is not cash.
### 3. Drive working capital

Receivables, payables, and inventory follow the user's days or a clearly labeled assumption. Do not plug cash to make the balance sheet balance without saying so.
### 4. Keep debt honest

Interest and principal follow the terms the user provided. If terms are missing, leave a labeled placeholder.
### 5. Balance check

Assets equal liabilities and equity, or you show the plug and refuse to hide it.
### 6. Document assumptions

A short list a reviewer can challenge. No circular story about growth funding itself unless the user describes that mechanism.

## Output

Deliver a **linked three-statement sketch**.

- Purpose of this linked three-statement sketch, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a linked three-statement sketch by 30 September 2026. An operator wants a 12-month view that shows why a profitable year can still run out of cash.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

An operator wants a 12-month view that shows why a profitable year can still run out of cash.

Historical statements or the fact that they are unavailable: Operating cash. Partly documented: the what is written down, the who is not
Forecast horizon: 13 weeks
Debt, capex, and working-capital drivers: Operating cash; Harbor & Co receipt. Both unassigned as of 14 September 2026
What decision the model must support: An operator wants a 12-month view that shows why a profitable year can still run out of cash
```

### Example outcome

**Linked three-statement sketch**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A linked sketch where the cash gap is explained by receivables and capex, with every assumption labeled and no hidden plug.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Historical statements or the fact that they are unavailable | Operating cash. Partly documented: the what is written down, the who is not | Needs confirmation |
| Forecast horizon | 13 weeks | Carried into the draft |
| Debt, capex, and working-capital drivers | Operating cash; Harbor & Co receipt. Both unassigned as of 14 September 2026 | Carried into the draft |
| What decision the model must support | An operator wants a 12-month view that shows why a profitable year can still run out of cash | Needs confirmation |

**How this draft was built**

**1. Start from the decision**  
Build only the detail that decision needs. A full monthly model is not automatically better.

**2. Link the statements**  
Net income flows to retained earnings. Depreciation, working capital, capex, and debt explain why profit is not cash.

**3. Drive working capital**  
Receivables, payables, and inventory follow the user's days or a clearly labeled assumption. Do not plug cash to make the balance sheet balance without saying so.

**4. Keep debt honest**  
Interest and principal follow the terms the user provided. If terms are missing, leave a labeled placeholder.

**5. Balance check**  
Assets equal liabilities and equity, or you show the plug and refuse to hide it.

**Deliberately not done**
- A P&L with a cash line typed in by hand and called a model.
- Hidden plugs.
- Invented debt terms.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A P&L with a cash line typed in by hand and called a model.
- Hidden plugs.
- Invented debt terms.

## Related skills

- `cash-flow-forecast`
- `working-capital`
- `financial-close-checklist`
