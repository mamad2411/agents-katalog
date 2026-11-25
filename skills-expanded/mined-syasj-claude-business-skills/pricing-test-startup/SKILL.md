---
name: pricing-test-startup
description: "Design a startup pricing test that learns willingness to pay without deceptive charges. Use when the user mentions pricing test, willingness to pay, test a price, startup pricing, or asks for a pricing test. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pricing-test-startup' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Startup Pricing Test

Design a startup pricing test that learns willingness to pay without deceptive charges.

## When to use this skill

Use this skill when the user:

- pricing test
- willingness to pay
- test a price
- startup pricing

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

- The offer
- The prices to test
- The buyer
- What must be disclosed

## Workflow


### 1. Step 1

Test a few prices, not a clever matrix they cannot staff.
### 2. Step 2

Disclose what the buyer will pay before they commit.
### 3. Define the evidence

paid, not 'interested'.
### 4. Step 4

Do not fake a crossed-out price or a false scarcity timer.
### 5. Step 5

Separate a price test from a promise you cannot deliver.
### 6. Step 6

Record the learning and the next price decision.

## Output

Deliver a **pricing test**.

- Purpose of this pricing test, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a pricing test by 30 September 2026. A test shows a 50 percent discount timer that resets for every visitor.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A test shows a 50 percent discount timer that resets for every visitor.

The offer: CAD 180, dates not set, cap not set
The prices to test: CAD 180
The buyer: Kite Freight
What must be disclosed: two deals cited from memory. Neither has a written loss reason
```

### Example outcome

**Pricing test**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the fake timer and counts paid commitments only.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The offer | CAD 180, dates not set, cap not set | Needs confirmation |
| The prices to test | CAD 180 | Carried into the draft |
| The buyer | Kite Freight | Carried into the draft |
| What must be disclosed | two deals cited from memory. Neither has a written loss reason | Needs confirmation |

**How this draft was built**

**1. Test a few prices, not a clever matrix they cannot staff**

**2. Disclose what the buyer will pay before they commit**

**3. Define the evidence**  
paid, not 'interested'.

**4. Do not fake a crossed-out price or a false scarcity timer**

**5. Separate a price test from a promise you cannot deliver**

**Deliberately not done**
- Hidden charges.
- Fake scarcity.
- Treating interest as payment.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Hidden charges
- Fake scarcity
- Treating interest as payment

## Related skills

- `pricing-packaging`
- `marketing-experiment`
