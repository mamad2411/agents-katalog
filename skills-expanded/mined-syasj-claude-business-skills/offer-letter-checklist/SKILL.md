---
name: offer-letter-checklist
description: "Prepare an offer checklist so compensation, start date, and conditions are complete before anyone celebrates. Use when the user mentions offer letter, prepare an offer, offer checklist, verbal offer, or asks for a offer checklist. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'offer-letter-checklist' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Offer Checklist

Prepare an offer checklist so compensation, start date, and conditions are complete before anyone celebrates.

## When to use this skill

Use this skill when the user:

- offer letter
- prepare an offer
- offer checklist
- verbal offer

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Role and level
- Compensation parts the company intends
- Start date and contingencies
- Approver

## Workflow


### 1. List the parts

Base, variable, equity if any, and benefits status. Do not invent numbers or equity values.
### 2. Contingencies

Background, work authorization, or other checks only if the user says they are part of the process. Do not invent a check.
### 3. Manager alignment

The hiring manager and the approver agree on level and pay band. If they do not, stop the checklist and surface the conflict.
### 4. Candidate-facing clarity

What is guaranteed versus discretionary, in plain language.
### 5. Expiration

An offer date and a response date the user chooses. Do not create false urgency.
### 6. Counsel and HR own the letter

This skill checks completeness. It does not declare the letter legally sufficient.

## Output

Deliver a **offer checklist**.

- Purpose of this offer checklist, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs an offer checklist by 30 September 2026. A manager told a candidate a number on a call, and finance has not approved the band.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A manager told a candidate a number on a call, and finance has not approved the band.

Role and level: Jordan Hale and one other, both unconfirmed as of 14 September 2026
Compensation parts the company intends: base CAD 60,000. Bonus line blank
Start date and contingencies: 30 September 2026
Approver: Chris Adeyemi. They have not signed
```

### Example outcome

**Offer checklist**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Blocks the letter until the band is approved and lists the verbal number as not yet an offer.

**Checklist**

- [x] **Role and level** — Jordan Hale and one other, both unconfirmed as of 14 September 2026  
      Evidenced in the file
- [x] **Compensation parts the company intends** — base CAD 60,000. Bonus line blank  
      Evidenced in the file
- [x] **Start date and contingencies** — 30 September 2026  
      Evidenced in the file
- [ ] **Approver** — Chris Adeyemi. They have not signed  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. List the parts
2. Contingencies
3. Manager alignment
4. Candidate-facing clarity
5. Expiration

**Deliberately not done**
- A verbal offer that omits variable-pay conditions.
- Invented equity value.
- False exploding-offer pressure.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Chris Adeyemi closes the open items before 30 September 2026.

## Anti-patterns

- A verbal offer that omits variable-pay conditions.
- Invented equity value.
- False exploding-offer pressure.

## Related skills

- `compensation-band`
- `employment-agreement-review`
- `onboarding-plan`
