---
name: planogram-brief
description: "Write a shelf placement brief that explains the logic behind the facing sequence and height allocation. Use when the user mentions planogram brief, shelf layout, shelf space, product placement retail, or asks for a planogram brief. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'planogram-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Planogram Brief

Write a shelf placement brief that explains the logic behind the facing sequence and height allocation.

## When to use this skill

Use this skill when the user:

- planogram brief
- shelf layout
- shelf space
- product placement retail

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

- The category
- Items competing for space
- Sales data they have
- Store layout constraints

## Workflow


### 1. Step 1

State the shopper path through the category first.
### 2. Step 2

Place high-turn and high-margin items at eye level using their data.
### 3. Step 3

Do not assign facings based on vendor pressure if it is not also in the data.
### 4. Step 4

Note seasonal items separately from core planogram.
### 5. Step 5

Keep a facing floor of one for items the buyer wants to test.
### 6. Step 6

Document who approved the sequence.

## Output

Deliver a **planogram brief**.

- Purpose of this planogram brief, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs a planogram brief by 30 September 2026. A brief gives 8 facings to a slow-selling line because the vendor paid for placement but does not disclose that.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A brief gives 8 facings to a slow-selling line because the vendor paid for placement but does not disclose that.

The category: SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached
Items competing for space: SKU 1044 cabin filter, last reviewed 14 September 2026. No owner named since
Sales data they have: Returns desk log, last reviewed 14 September 2026. No owner named since
Store layout constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Planogram brief**
To: Diane Cho, store lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Uses their sales data and labels any placement that is not data-driven.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The category | SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Items competing for space | SKU 1044 cabin filter, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Sales data they have | Returns desk log, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Store layout constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. State the shopper path through the category first**

**2. Place high-turn and high-margin items at eye level using their data**

**3. Do not assign facings based on vendor pressure if it is not also in the data**

**4. Note seasonal items separately from core planogram**

**5. Keep a facing floor of one for items the buyer wants to test**

**Deliberately not done**
- Vendor pressure disguised as a sales rule.
- Facings with no data basis.
- Missing seasonal note.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Vendor pressure disguised as a sales rule
- Facings with no data basis
- Missing seasonal note

## Related skills

- `assortment-review`
- `inventory-policy`
