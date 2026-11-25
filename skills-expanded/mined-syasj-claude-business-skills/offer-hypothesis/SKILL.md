---
name: offer-hypothesis
description: "Frame a startup offer as a hypothesis with a buyer, a promise, and a test. Use when the user mentions offer hypothesis, startup offer, what are we selling, test the offer, or asks for a offer hypothesis. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'offer-hypothesis' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Offer Hypothesis

Frame a startup offer as a hypothesis with a buyer, a promise, and a test.

## When to use this skill

Use this skill when the user:

- offer hypothesis
- startup offer
- what are we selling
- test the offer

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

- The buyer
- The promise
- The alternative
- The test they can run

## Workflow


### 1. Step 1

Name one buyer and one painful job.
### 2. Step 2

Write the promise in concrete terms.
### 3. Step 3

State the alternative they use now.
### 4. Design a test that can fail

a paid pilot, a letter, or a concierge week.
### 5. Step 5

Define the kill metric before the test.
### 6. Step 6

Do not invent traction, waitlists, or investor interest.

## Output

Deliver a **offer hypothesis**.

- Purpose of this offer hypothesis, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs an offer hypothesis by 30 September 2026. A deck says thousands of users want the product, and no user has been asked.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A deck says thousands of users want the product, and no user has been asked.

The buyer: Cedar Clinic
The promise: none written down beyond the ask
The alternative: two deals cited from memory. Neither has a written loss reason
The test they can run: First four paying accounts, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Offer hypothesis**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A hypothesis and a small test, with the invented user count removed.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The buyer | Cedar Clinic | Needs confirmation |
| The promise | none written down beyond the ask | Carried into the draft |
| The alternative | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| The test they can run | First four paying accounts, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Name one buyer and one painful job**

**2. Write the promise in concrete terms**

**3. State the alternative they use now**

**4. Design a test that can fail**  
a paid pilot, a letter, or a concierge week.

**5. Define the kill metric before the test**

**Deliberately not done**
- Invented traction.
- A test that cannot fail.
- Five buyers in one hypothesis.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented traction
- A test that cannot fail
- Five buyers in one hypothesis

## Related skills

- `experiment-design`
- `product-brief`
