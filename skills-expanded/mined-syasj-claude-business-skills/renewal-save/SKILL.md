---
name: renewal-save
description: "Plan a renewal that is at risk by finding the real grievance and offering a remedy inside policy. Use when the user mentions renewal risk, save a customer, churning customer, renewal negotiation, or asks for a renewal save plan. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'renewal-save' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Renewal Save

Plan a renewal that is at risk by finding the real grievance and offering a remedy inside policy.

## When to use this skill

Use this skill when the user:

- renewal risk
- save a customer
- churning customer
- renewal negotiation

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

- What the customer says is wrong
- Usage or value evidence the user has
- What concessions are authorized
- The renewal date

## Workflow


### 1. Grievance

Write the customer's complaint without defending the company first.
### 2. Value evidence

What outcomes did happen, using their data. Do not invent usage.
### 3. Cause

Product gap, adoption gap, or commercial mismatch. The remedy depends on the cause.
### 4. Remedy

A plan, a scope change, or a concession within authority. No unauthorized discount and no blame-the-customer email.
### 5. Executive path

When a leader should join, and what they should say. No surprise discounts from a founder.
### 6. Decision date

The date the customer will decide, if they gave one. Do not invent urgency.

## Output

Deliver a **renewal save plan**.

- Purpose of this renewal save plan, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a renewal save plan by 30 September 2026. A customer will not renew because nobody completed onboarding, and the rep wants to offer 30 percent off.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A customer will not renew because nobody completed onboarding, and the rep wants to offer 30 percent off.

What the customer says is wrong: Redline Parts, last reviewed 14 September 2026. No owner named since
Usage or value evidence the user has: one PDF, 2 pages, dated 14 September 2026
What concessions are authorized: Redline Parts, last reviewed 14 September 2026. No owner named since
The renewal date: 30 September 2026
```

### Example outcome

**Renewal save plan**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Leads with an onboarding remedy and holds the discount until a commercial problem is actually shown.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What the customer says is wrong | Redline Parts, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Usage or value evidence the user has | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| What concessions are authorized | Redline Parts, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The renewal date | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Grievance**  
Write the customer's complaint without defending the company first.

**2. Value evidence**  
What outcomes did happen, using their data. Do not invent usage.

**3. Cause**  
Product gap, adoption gap, or commercial mismatch. The remedy depends on the cause.

**4. Remedy**  
A plan, a scope change, or a concession within authority. No unauthorized discount and no blame-the-customer email.

**5. Executive path**  
When a leader should join, and what they should say. No surprise discounts from a founder.

**Deliberately not done**
- A discount as the first response to an adoption problem.
- Invented usage statistics.
- A defensive email that argues the customer is wrong.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A discount as the first response to an adoption problem.
- Invented usage statistics.
- A defensive email that argues the customer is wrong.

## Related skills

- `churn-interview`
- `account-plan`
