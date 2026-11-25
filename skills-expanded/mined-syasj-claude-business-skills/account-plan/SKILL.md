---
name: account-plan
description: "Write an account plan for a named customer that focuses on their goals, the whitespace you can evidence, and the next plays. Use when the user mentions account plan, strategic account, land and expand plan, account strategy, or asks for a account plan. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'account-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Account Plan

Write an account plan for a named customer that focuses on their goals, the whitespace you can evidence, and the next plays.

## When to use this skill

Use this skill when the user:

- account plan
- strategic account
- land and expand plan
- account strategy

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The customer's stated goals
- Current products and stakeholders
- Whitespace you can evidence
- Risks to the relationship

## Workflow


### 1. Customer goals first

Their goals, not your quota, open the plan.
### 2. Map

Stakeholders you actually know, with roles. Do not invent an org chart.
### 3. Whitespace

Opportunities tied to a goal. A product list is not whitespace.
### 4. Risks

Champion departure, unresolved support issues, or competitive evaluations they mentioned.
### 5. Plays

At most three plays this quarter, each with an owner and a buyer action.
### 6. Internal ask

What the account needs from product or support. No private complaints without a request.

## Output

Deliver a **account plan**.

- Purpose of this account plan, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs an account plan by 30 September 2026. An account manager owns a renewal and wants a strategic plan, but the only known goal is 'get through this year's audit'.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

An account manager owns a renewal and wants a strategic plan, but the only known goal is 'get through this year's audit'.

The customer's stated goals: An account manager owns a renewal and wants a strategic plan, but the only known goal is 'get through this year's audit'. Stated once, in the ask. Not written down anywhere else
Current products and stakeholders: Samir Qureshi plus two others named in the thread. No distribution list attached
Whitespace you can evidence: one PDF, 2 pages, dated 14 September 2026
Risks to the relationship: Harbor Goods is open. No score in the file
```

### Example outcome

**Account plan**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A plan anchored on the audit goal, with one evidenced expansion idea and the rest marked unknown.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The customer's stated goals | An account manager owns a renewal and wants a strategic plan, but the only known goal is 'get through this year's audit'. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Current products and stakeholders | Samir Qureshi plus two others named in the thread. No distribution list attached | Carried into the draft |
| Whitespace you can evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Risks to the relationship | Harbor Goods is open. No score in the file | Needs confirmation |

**How this draft was built**

**1. Customer goals first**  
Their goals, not your quota, open the plan.

**2. Map**  
Stakeholders you actually know, with roles. Do not invent an org chart.

**3. Whitespace**  
Opportunities tied to a goal. A product list is not whitespace.

**4. Risks**  
Champion departure, unresolved support issues, or competitive evaluations they mentioned.

**5. Plays**  
At most three plays this quarter, each with an owner and a buyer action.

**Deliberately not done**
- A plan that is only a quota target.
- Invented stakeholders.
- Twelve plays and no owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A plan that is only a quota target.
- Invented stakeholders.
- Twelve plays and no owner.

## Related skills

- `champion-map`
- `qbr-customer`
