---
name: runway-choice
description: "State the runway choice from cash, burn, and the hire they are considering. Use when the user mentions runway, how long is our cash, hire or wait, burn choice, or asks for a runway note. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'runway-choice' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Runway Choice

State the runway choice from cash, burn, and the hire they are considering.

## When to use this skill

Use this skill when the user:

- runway
- how long is our cash
- hire or wait
- burn choice

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Startup advice is a set of choices, not a promise of funding or growth. Do not invent traction, customers, or investor interest.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Cash
- Monthly burn
- The hire cost
- The date they care about

## Workflow


### 1. Step 1

Use their cash and burn.
### 2. Step 2

Show months at the current burn.
### 3. Step 3

Show months if the hire starts.
### 4. Step 4

Do not treat a maybe receivable as cash.
### 5. Step 5

Recommend one choice.
### 6. Step 6

Do not promise a raise.

## Output

Deliver a **runway note**.

- Purpose of this runway note, in two sentences.
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

Northline has $180,000 cash. Burn is $30,000 a month. A hire would add $8,000. A customer might pay $40,000. Mara wants to know if she can hire.

### Example data

```text
cash: 180000
monthly burn: 30000
hire: 8000 a month, not started
maybe receipt: 40000, not in the bank
date she cares about: 31 Mar 2027
```

### Example outcome

**Runway**
Current burn: 180,000 / 30,000 = 6 months. That is the file, not a promise.
With the hire: 38,000 a month, under 5 months. Do not start the hire on this note.
The $40,000 stays out. It is not cash.
No raise is assumed.
Choice: wait. Revisit if the $40,000 arrives.

## Anti-patterns

- A receivable counted as cash
- A raise assumed
- Burn without the hire shown separately

## Related skills

- `runway-and-burn`
- `cash-flow-forecast`
