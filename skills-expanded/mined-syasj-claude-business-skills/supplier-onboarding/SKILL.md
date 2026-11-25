---
name: supplier-onboarding
description: "Onboard a supplier with the documents, access, and first-order check the company actually requires. Use when the user mentions supplier onboarding, new vendor setup, supplier setup, vendor onboarding, or asks for a supplier onboarding checklist. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'supplier-onboarding' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Supplier Onboarding

Onboard a supplier with the documents, access, and first-order check the company actually requires.

## When to use this skill

Use this skill when the user:

- supplier onboarding
- new vendor setup
- supplier setup
- vendor onboarding

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Inventory and supplier recommendations depend on the user's lead times and service targets. Do not invent supplier performance.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Required documents
- Risk tier
- System access needed
- The first order

## Workflow


### 1. Step 1

Collect only documents their policy requires.
### 2. Step 2

Match the review depth to the risk tier.
### 3. Step 3

Set up access for named people, not a shared login.
### 4. Step 4

Confirm payment details through their verified channel. Do not accept a change from an unverified email.
### 5. Step 5

Define a successful first order.
### 6. Step 6

Refuse any request to skip sanctions or payment verification they already require.

## Output

Deliver a **supplier onboarding checklist**.

- Purpose of this supplier onboarding checklist, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a supplier onboarding checklist by 30 September 2026. A supplier emails new bank details from a free mail account and wants the next payment sent there.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A supplier emails new bank details from a free mail account and wants the next payment sent there.

Required documents: one PDF, 2 pages, dated 14 September 2026
Risk tier: SKU 1044 cabin filter is open. No score in the file
System access needed: the one named in the ask. Version and owner not recorded
The first order: SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Supplier onboarding checklist**
Harbor Goods · 14 September 2026 · Due 30 September 2026

**Decision**
Blocks the change until their verified channel confirms it.

**Checklist**

- [x] **Required documents** — one PDF, 2 pages, dated 14 September 2026  
      Evidenced in the file
- [x] **Risk tier** — SKU 1044 cabin filter is open. No score in the file  
      Evidenced in the file
- [x] **System access needed** — the one named in the ask. Version and owner not recorded  
      Evidenced in the file
- [ ] **The first order** — SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Collect only documents their policy requires
2. Match the review depth to the risk tier
3. Set up access for named people, not a shared login
4. Confirm payment details through their verified channel. Do not accept a change from an unverified email
5. Define a successful first order

**Deliberately not done**
- A shared vendor login.
- Payment detail changes from unverified email.
- Skipping a required check.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Diane Cho closes the open items before 30 September 2026.

## Anti-patterns

- A shared vendor login
- Payment detail changes from unverified email
- Skipping a required check

## Related skills

- `purchase-order-control`
- `sanctions-compliance-process`
