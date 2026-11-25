---
name: treasury-policy-brief
description: "Draft the questions and structure of a simple cash and risk policy for a small finance team. Use when the user mentions treasury policy, cash policy, who can move money, investment of surplus cash, or asks for a treasury policy brief. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'treasury-policy-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Treasury Policy Brief

Draft the questions and structure of a simple cash and risk policy for a small finance team.

## When to use this skill

Use this skill when the user:

- treasury policy
- cash policy
- who can move money
- investment of surplus cash

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

- Entities and bank relationships the user mentioned
- Who may approve payments today
- Surplus cash, if any
- Risks they have already hit

## Workflow


### 1. Write the purpose

Safeguard cash, pay on time, and avoid surprises. Do not turn a small company policy into a bank manual.
### 2. Approval matrix

Recommend they document who can approve which payment size. Use their current practice as the starting point and flag gaps.
### 3. Account rules

Which accounts exist and why, in their description. Suggest fewer accounts if they described confusion, and explain why.
### 4. Surplus cash

If they park cash, list policy questions: access, credit quality, and who decides. Do not recommend a product or a yield.
### 5. Exceptions

How an emergency payment is approved and recorded the next day.
### 6. Do not ask for logins

Policy work does not need passwords, tokens, or card numbers.

## Output

Deliver a **treasury policy brief**.

- Purpose of this treasury policy brief, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a treasury policy brief by 30 September 2026. A controller wants a one-page cash policy after a duplicate payment slipped through.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A controller wants a one-page cash policy after a duplicate payment slipped through.

Entities and bank relationships the user mentioned: Harbor & Co receipt. Stated in the ask, not documented anywhere else
Who may approve payments today: Mara Chen, founder
Surplus cash, if any: Operating cash, recorded 14 September 2026. No supporting file attached
Risks they have already hit: Operating cash is open. No score in the file
```

### Example outcome

**Treasury policy brief**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A policy brief with an approval matrix, an exception path, and no request for credentials or product pitches.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Entities and bank relationships the user mentioned | Harbor & Co receipt. Stated in the ask, not documented anywhere else | Needs confirmation |
| Who may approve payments today | Mara Chen, founder | Carried into the draft |
| Surplus cash, if any | Operating cash, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Risks they have already hit | Operating cash is open. No score in the file | Needs confirmation |

**How this draft was built**

**1. Write the purpose**  
Safeguard cash, pay on time, and avoid surprises. Do not turn a small company policy into a bank manual.

**2. Approval matrix**  
Recommend they document who can approve which payment size. Use their current practice as the starting point and flag gaps.

**3. Account rules**  
Which accounts exist and why, in their description. Suggest fewer accounts if they described confusion, and explain why.

**4. Surplus cash**  
If they park cash, list policy questions: access, credit quality, and who decides. Do not recommend a product or a yield.

**5. Exceptions**  
How an emergency payment is approved and recorded the next day.

**Deliberately not done**
- A hedge fund investment policy for a company with one operating account.
- Requesting banking credentials to 'set up the policy'.
- Promising a return on surplus cash.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A hedge fund investment policy for a company with one operating account.
- Requesting banking credentials to 'set up the policy'.
- Promising a return on surplus cash.

## Related skills

- `fx-exposure-review`
- `internal-controls-walkthrough`
- `cash-flow-forecast`
