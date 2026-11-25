---
name: assortment-review
description: "Review an assortment for the customer job, the duplicate, and the item that does not earn its space. Use when the user mentions assortment review, range review, what to drop, planogram logic, or asks for a assortment review. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'assortment-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Assortment Review

Review an assortment for the customer job, the duplicate, and the item that does not earn its space.

## When to use this skill

Use this skill when the user:

- assortment review
- range review
- what to drop
- planogram logic

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

- Items and sales they have
- Space
- The customer job
- Known stockouts

## Workflow


### 1. Step 1

Group items by the job the shopper is solving.
### 2. Step 2

Flag duplicates that do not change a choice.
### 3. Step 3

Note stockouts separately from slow sellers.
### 4. Step 4

Recommend a drop, a keep, or a test using their sales.
### 5. Step 5

Do not invent a trend to justify a pet product.
### 6. Step 6

Leave seasonal exit dates visible.

## Output

Deliver a **assortment review**.

- Purpose of this assortment review, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs an assortment review by 30 September 2026. A slow-seller list includes an item that was empty for a month.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A slow-seller list includes an item that was empty for a month.

Items and sales they have: SKU 1044 cabin filter, last reviewed 14 September 2026. No owner named since
Space: End-cap display 3, recorded 14 September 2026. No supporting file attached
The customer job: the shopper solving one task in one trip. Not segmented further in the file
Known stockouts: End-cap display 3. Stated in the ask, not documented anywhere else
```

### Example outcome

**Assortment review**
To: Diane Cho, store lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Separates the stockout from true slow sellers before any drop.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Items and sales they have | SKU 1044 cabin filter, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Space | End-cap display 3, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The customer job | the shopper solving one task in one trip. Not segmented further in the file | Carried into the draft |
| Known stockouts | End-cap display 3. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Group items by the job the shopper is solving**

**2. Flag duplicates that do not change a choice**

**3. Note stockouts separately from slow sellers**

**4. Recommend a drop, a keep, or a test using their sales**

**5. Do not invent a trend to justify a pet product**

**Deliberately not done**
- An invented trend.
- Cutting a stocked-out item as if it were unwanted.
- No customer job.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An invented trend
- Cutting a stocked-out item as if it were unwanted
- No customer job

## Related skills

- `inventory-policy`
- `demand-plan-review`
