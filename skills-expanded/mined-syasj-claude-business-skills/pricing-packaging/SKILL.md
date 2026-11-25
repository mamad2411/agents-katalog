---
name: pricing-packaging
description: "Frame a pricing and packaging decision as a set of fences and a test, not as a number pulled from a competitor. Use when the user mentions pricing and packaging, package tiers, price a product, packaging review, or asks for a packaging recommendation. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pricing-packaging' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Pricing and Packaging

Frame a pricing and packaging decision as a set of fences and a test, not as a number pulled from a competitor.

## When to use this skill

Use this skill when the user:

- pricing and packaging
- package tiers
- price a product
- packaging review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The buyer and the value unit
- Current price and packaging
- Costs that constrain price
- What sales keeps conceding

## Workflow


### 1. Value unit

What the customer expects to pay for. Seat, usage, or outcome, in their language.
### 2. Fences

What differs between packages, and why a buyer would upgrade. Cosmetic fences are a finding.
### 3. Cost floor

Use their cost facts. Do not invent a margin target.
### 4. Concessions

What sales gives away is part of the real price. Include it.
### 5. Test

A limited price or package test with a decision rule, rather than a company-wide leap, when evidence is thin.
### 6. Honesty

No hidden fees in the recommendation. Counsel reviews consumer-facing terms if the user says they are required.

## Output

Deliver a **packaging recommendation**.

- Purpose of this packaging recommendation, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs a packaging recommendation by 30 September 2026. The company has three tiers that differ only by a feature nobody uses, and discounting is constant.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The company has three tiers that differ only by a feature nobody uses, and discounting is constant.

The buyer and the value unit: Activation checklist, recorded 14 September 2026. No supporting file attached
Current price and packaging: CAD 180
Costs that constrain price: CAD 180
What sales keeps conceding: Usage limit warning, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Packaging recommendation**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Treats the discount as the real price and proposes a clearer fence to test.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The buyer and the value unit | Activation checklist, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Current price and packaging | CAD 180 | Carried into the draft |
| Costs that constrain price | CAD 180 | Carried into the draft |
| What sales keeps conceding | Usage limit warning, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Value unit**  
What the customer expects to pay for. Seat, usage, or outcome, in their language.

**2. Fences**  
What differs between packages, and why a buyer would upgrade. Cosmetic fences are a finding.

**3. Cost floor**  
Use their cost facts. Do not invent a margin target.

**4. Concessions**  
What sales gives away is part of the real price. Include it.

**5. Test**  
A limited price or package test with a decision rule, rather than a company-wide leap, when evidence is thin.

**Deliberately not done**
- Copying a competitor's price with no context.
- Hidden fees.
- Tiers that do not change the value.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Copying a competitor's price with no context.
- Hidden fees.
- Tiers that do not change the value.

## Related skills

- `pricing-margin-bridge`
- `offer-design`
