---
name: marketplace-fee-review
description: "Review a marketplace fee structure and show the net margin per unit at their price. Use when the user mentions marketplace fees, amazon fees, platform fees, seller fees, or asks for a marketplace fee review. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'marketplace-fee-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Marketplace Fee Review

Review a marketplace fee structure and show the net margin per unit at their price.

## When to use this skill

Use this skill when the user:

- marketplace fees
- amazon fees
- platform fees
- seller fees
- net margin marketplace

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent inventory, prices, or reviews. Do not write deceptive promotions.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Their selling price
- Their unit cost
- The fee schedule they shared
- Fulfillment method

## Workflow


### 1. Step 1

Apply each fee line from the schedule they supplied. Do not invent a fee category.
### 2. Step 2

Show the net per unit and the margin percentage.
### 3. Step 3

Flag any fee that changes at volume thresholds they provided.
### 4. Step 4

If a fee is missing from their schedule, say so rather than estimating.
### 5. Step 5

FBA versus FBM comparison only if they asked for both.

## Output

Deliver a **marketplace fee review**.

- Purpose of this marketplace fee review, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs a marketplace fee review by 30 September 2026. A review uses last year's referral fee rate and shows a margin that is no longer achievable.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A review uses last year's referral fee rate and shows a margin that is no longer achievable.

Their selling price: CAD 79
Their unit cost: CAD 36 direct. Overhead not in this line
The fee schedule they shared: CAD 79, from their sheet, not a guess
Fulfillment method: the method in the ask. No second design attached
```

### Example outcome

**Marketplace fee review**
To: Diane Cho, store lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A review built from the fee schedule they pasted and a note to verify the date.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Their selling price | CAD 79 | Needs confirmation |
| Their unit cost | CAD 36 direct. Overhead not in this line | Carried into the draft |
| The fee schedule they shared | CAD 79, from their sheet, not a guess | Carried into the draft |
| Fulfillment method | the method in the ask. No second design attached | Needs confirmation |

**How this draft was built**

**1. Apply each fee line from the schedule they supplied. Do not invent a fee category**

**2. Show the net per unit and the margin percentage**

**3. Flag any fee that changes at volume thresholds they provided**

**4. If a fee is missing from their schedule, say so rather than estimating**

**5. FBA versus FBM comparison only if they asked for both**

**Deliberately not done**
- Invented fee rates.
- Confirming margin without seeing the actual cost.
- Mixing fee years.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented fee rates
- Confirming margin without seeing the actual cost
- Mixing fee years

## Related skills

- None in this domain yet. Use the skill finder if the task sits elsewhere.
