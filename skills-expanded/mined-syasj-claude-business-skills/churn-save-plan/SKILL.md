---
name: churn-save-plan
description: "Plan a save offer from the cancel reasons in the export and the offer they can honor. Use when the user mentions churn save, cancel flow, save offer, why are they leaving, or asks for a save plan. SaaS skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: saas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'churn-save-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Churn Save Plan

Plan a save offer from the cancel reasons in the export and the offer they can honor.

## When to use this skill

Use this skill when the user:

- churn save
- cancel flow
- save offer
- why are they leaving

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent churn, revenue, retention, or a security certification. If the export is missing, say so.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Cancel reasons
- Counts
- The offer they can honor
- Who approves a credit

## Workflow


### 1. Step 1

Rank reasons by their counts.
### 2. Step 2

Match an offer only to a reason it can fix.
### 3. Step 3

A price save does not fix a missing feature.
### 4. Step 4

Use only credits they authorized.
### 5. Step 5

Do not invent a save rate.
### 6. Step 6

Name the approver.

## Output

Deliver a **save plan**.

- Purpose of this save plan, in two sentences.
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

Forty cancels in August. Twenty-two said the export they need does not exist. Ten said price. Eight gave no reason. A draft offers 20 percent off to all forty. Jonah can approve a 10 percent credit, not 20.

### Example data

```text
cancels: 40, August 2026
missing export: 22
price: 10
no reason: 8
credit he can approve: 10 percent, one month
20 percent draft: not approved
```

### Example outcome

**Save plan**
Do not discount the 22. A cheaper plan does not create the missing export.
Price reason, 10 accounts: a 10 percent credit for one month is the offer he can honor. Not 20.
No reason, 8: no offer. Ask, or leave them.
No save rate is claimed. None was measured.
Approver for the credit: Jonah.

## Anti-patterns

- One offer for every reason
- An unauthorized credit
- A fake save rate

## Related skills

- `saas-weekly-metrics`
- `renewal-save`
