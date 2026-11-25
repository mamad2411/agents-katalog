---
name: product-listing-review
description: "Review an online product listing for accurate claims, complete specs, and images that match what ships. Use when the user mentions product listing review, listing copy review, PDP review, online product page, or asks for a product listing review. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'product-listing-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Product Listing Review

Review an online product listing for accurate claims, complete specs, and images that match what ships.

## When to use this skill

Use this skill when the user:

- product listing review
- listing copy review
- PDP review
- online product page

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

- The current listing copy
- Product specs they confirmed
- Images available
- Category restrictions

## Workflow


### 1. Step 1

Check every claim against the specs they supplied. Flag anything that cannot be confirmed.
### 2. Step 2

Identify missing dimensions, materials, or compatibility notes a buyer needs.
### 3. Step 3

Images must show what ships, at the quantity shown. Do not approve images of a bundle not included.
### 4. Step 4

No invented reviews, fake ratings, or implied endorsements.
### 5. Step 5

Follow category restrictions if the user named them.
### 6. Step 6

Flag any claim that could trigger a misleading-advertising complaint.

## Output

Deliver a **product listing review**.

- Purpose of this product listing review, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs a product listing review by 30 September 2026. A listing says the item includes a charger but the SKU does not ship one.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A listing says the item includes a charger but the SKU does not ship one.

The current listing copy: SKU 1044 cabin filter; End-cap display 3; Returns desk log
Product specs they confirmed: SKU 1044 cabin filter. Stated in the ask, not documented anywhere else
Images available: End-cap display 3 and one other, both unconfirmed as of 14 September 2026
Category restrictions: SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Product listing review**
To: Diane Cho, store lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the charger claim and flags the image showing one.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The current listing copy | SKU 1044 cabin filter; End-cap display 3; Returns desk log | Needs confirmation |
| Product specs they confirmed | SKU 1044 cabin filter. Stated in the ask, not documented anywhere else | Carried into the draft |
| Images available | End-cap display 3 and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Category restrictions | SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Check every claim against the specs they supplied. Flag anything that cannot be confirmed**

**2. Identify missing dimensions, materials, or compatibility notes a buyer needs**

**3. Images must show what ships, at the quantity shown. Do not approve images of a bundle not included**

**4. No invented reviews, fake ratings, or implied endorsements**

**5. Follow category restrictions if the user named them**

**Deliberately not done**
- Invented specs.
- Images of items not in the package.
- Fake social proof.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented specs
- Images of items not in the package
- Fake social proof

## Related skills

- `marketing-claims-review`
- `promotion-review`
