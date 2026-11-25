---
name: property-listing-brief
description: "Brief a property listing from facts the owner confirmed, with no invented features. Use when the user mentions listing brief, property description, write a listing, marketing a property, or asks for a listing brief. Real estate skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: real-estate
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'property-listing-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Property Listing Brief

Brief a property listing from facts the owner confirmed, with no invented features.

## When to use this skill

Use this skill when the user:

- listing brief
- property description
- write a listing
- marketing a property

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not brokerage, appraisal, or legal advice. Do not invent comparable sales, rents, or legal rights. A licensed local professional must confirm any transaction.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Confirmed features
- Known defects they disclosed
- The audience
- Claims they must not make

## Workflow


### 1. Step 1

Use only confirmed features.
### 2. Step 2

Disclose known material defects they told you about. Do not help hide them.
### 3. Step 3

Separate lifestyle copy from measurable facts.
### 4. Step 4

Do not invent school quality, income, or a legal use.
### 5. Step 5

Mark what a buyer must verify.
### 6. Step 6

This is not a valuation.

## Output

Deliver a **listing brief**.

- Purpose of this listing brief, in two sentences.
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

Helen Cho, property manager at Cedar Street Properties in Airdrie, needs a listing brief by 30 September 2026. A draft says the unit rents for a number the owner has not achieved.

### Example data

```text
From: Helen Cho, property manager
Organization: Cedar Street Properties, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A draft says the unit rents for a number the owner has not achieved.

Confirmed features: Unit 4B lease. Stated in the ask, not documented anywhere else
Known defects they disclosed: two deals cited from memory. Neither has a written loss reason
The audience: people who already buy from Cedar Street Properties
Claims they must not make: the draft sentence is broader than the note
```

### Example outcome

**Listing brief**
To: Helen Cho, property manager, Cedar Street Properties
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the invented rent and lists defects the owner already disclosed.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Confirmed features | Unit 4B lease. Stated in the ask, not documented anywhere else | Needs confirmation |
| Known defects they disclosed | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| The audience | people who already buy from Cedar Street Properties | Carried into the draft |
| Claims they must not make | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Use only confirmed features**

**2. Disclose known material defects they told you about. Do not help hide them**

**3. Separate lifestyle copy from measurable facts**

**4. Do not invent school quality, income, or a legal use**

**5. Mark what a buyer must verify**

**Deliberately not done**
- Hidden defects.
- Invented income.
- A valuation disguised as a listing.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Helen Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Hidden defects
- Invented income
- A valuation disguised as a listing

## Related skills

- `marketing-claims-review`
- `property-due-diligence`
