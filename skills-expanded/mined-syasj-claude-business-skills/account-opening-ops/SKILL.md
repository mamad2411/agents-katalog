---
name: account-opening-ops
description: "Review an account-opening checklist for identity steps they require, without collecting secrets into the chat. Use when the user mentions account opening, KYC checklist, onboarding a customer bank, new account ops, or asks for a account-opening checklist. Banking and treasury operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: banking
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'account-opening-ops' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Account Opening Operations

Review an account-opening checklist for identity steps they require, without collecting secrets into the chat.

## When to use this skill

Use this skill when the user:

- account opening
- KYC checklist
- onboarding a customer bank
- new account ops

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

- Their required steps
- What is complete
- Exceptions
- The reviewer

## Workflow


### 1. Step 1

Use their checklist. Do not invent a regulator's rule.
### 2. Step 2

Note missing identity steps as gaps.
### 3. Step 3

Do not ask customers to send passwords or full card data by chat.
### 4. Step 4

Exceptions need their compliance owner.
### 5. Step 5

A possible sanctions match follows their screening process. Do not suggest altering a name.
### 6. Step 6

This is operations support, not a license to open the account.

## Output

Deliver a **account-opening checklist**.

- Purpose of this account-opening checklist, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an account-opening checklist by 30 September 2026. Staff want to skip an identity step because the customer is in a hurry.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Staff want to skip an identity step because the customer is in a hurry.

Their required steps: Payment run 14 Sep; Account opening file 221. Both unassigned as of 14 September 2026
What is complete: Liquidity ladder, last reviewed 14 September 2026. No owner named since
Exceptions: Payment run 14 Sep is open. Account opening file 221 was raised verbally and never logged
The reviewer: Priya Shah. No second reviewer named
```

### Example outcome

**Account-opening checklist**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Keeps the step and routes any exception to the compliance owner.

**Checklist**

- [x] **Their required steps** — Payment run 14 Sep; Account opening file 221. Both unassigned as of 14 September 2026  
      Evidenced in the file
- [x] **What is complete** — Liquidity ladder, last reviewed 14 September 2026. No owner named since  
      Evidenced in the file
- [x] **Exceptions** — Payment run 14 Sep is open. Account opening file 221 was raised verbally and never logged  
      Evidenced in the file
- [ ] **The reviewer** — Priya Shah. No second reviewer named  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Use their checklist. Do not invent a regulator's rule
2. Note missing identity steps as gaps
3. Do not ask customers to send passwords or full card data by chat
4. Exceptions need their compliance owner
5. A possible sanctions match follows their screening process. Do not suggest altering a name

**Deliberately not done**
- Invented regulatory rules.
- Name changes to dodge screening.
- Secrets collected in chat.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Priya Shah closes the open items before 30 September 2026.

## Anti-patterns

- Invented regulatory rules
- Name changes to dodge screening
- Secrets collected in chat

## Related skills

- `sanctions-compliance-process`
