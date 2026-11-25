---
name: lease-abstract
description: "Abstract a lease the user provides into dates, money, and notice clauses, without a legal opinion. Use when the user mentions lease abstract, summarize a lease, lease dates, rent roll support, or asks for a lease abstract. Real estate skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: real-estate
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'lease-abstract' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Lease Abstract

Abstract a lease the user provides into dates, money, and notice clauses, without a legal opinion.

## When to use this skill

Use this skill when the user:

- lease abstract
- summarize a lease
- lease dates
- rent roll support

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

- The lease text
- The questions they need answered
- Amendments they have
- Who will rely on it

## Workflow


### 1. Step 1

Quote dates, rent, and notice periods from the text.
### 2. Step 2

Flag missing pages or amendments.
### 3. Step 3

Do not assume a renewal right that is not written.
### 4. Step 4

Separate what the lease says from what the tenant hopes.
### 5. Step 5

List questions for counsel.
### 6. Step 6

Do not calculate a legal default.

## Output

Deliver a **lease abstract**.

- Purpose of this lease abstract, in two sentences.
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

Helen Cho, property manager at Cedar Street Properties in Airdrie, needs a lease abstract by 30 September 2026. An abstract assumes a five-year renewal the lease only mentions as a negotiation.

### Example data

```text
From: Helen Cho, property manager
Organization: Cedar Street Properties, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

An abstract assumes a five-year renewal the lease only mentions as a negotiation.

The lease text: Unit 4B lease, recorded 14 September 2026. No supporting file attached
The questions they need answered: An abstract assumes a five-year renewal the lease only mentions as a negotiation
Amendments they have: Rent roll, 12 units. Stated in the ask, not documented anywhere else
Who will rely on it: Helen Cho, property manager
```

### Example outcome

**Lease abstract**
To: Helen Cho, property manager, Cedar Street Properties
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Marks renewal as unwritten and lists the counsel question.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The lease text | Unit 4B lease, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The questions they need answered | An abstract assumes a five-year renewal the lease only mentions as a negotiation | Carried into the draft |
| Amendments they have | Rent roll, 12 units. Stated in the ask, not documented anywhere else | Carried into the draft |
| Who will rely on it | Helen Cho, property manager | Needs confirmation |

**How this draft was built**

**1. Quote dates, rent, and notice periods from the text**

**2. Flag missing pages or amendments**

**3. Do not assume a renewal right that is not written**

**4. Separate what the lease says from what the tenant hopes**

**5. List questions for counsel**

**Deliberately not done**
- Assumed renewal rights.
- A legal default opinion.
- An abstract of a missing page.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Helen Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Assumed renewal rights
- A legal default opinion
- An abstract of a missing page

## Related skills

- `contract-risk-review`
- `rent-roll-review`
