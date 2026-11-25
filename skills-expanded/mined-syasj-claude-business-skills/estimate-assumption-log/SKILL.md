---
name: estimate-assumption-log
description: "Log estimate assumptions so a bid can be explained without invented quantities. Use when the user mentions estimate assumptions, bid assumptions, quantity assumptions, estimating log, or asks for a assumption log. Construction skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: construction
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'estimate-assumption-log' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Estimate Assumption Log

Log estimate assumptions so a bid can be explained without invented quantities.

## When to use this skill

Use this skill when the user:

- estimate assumptions
- bid assumptions
- quantity assumptions
- estimating log

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Site safety and contract administration follow the contract and the site rules. Do not tell anyone to skip a safety control. Do not invent quantities.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The scope basis
- Quantities they measured
- Allowances
- Exclusions

## Workflow


### 1. Step 1

State the documents the estimate is based on.
### 2. Step 2

List quantities as measured or as an allowance.
### 3. Step 3

Write exclusions plainly.
### 4. Step 4

Do not invent a productivity rate and call it fact. Label judgments.
### 5. Step 5

Note what a missing drawing would change.
### 6. Step 6

This is not a bid strategy to mislead a client. The log should make the price understandable.

## Output

Deliver a **assumption log**.

- Purpose of this assumption log, in two sentences.
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

Tom Reilly, site lead at Birch Siteworks in Cochrane, needs an assumption log by 30 September 2026. An estimate assumes night work is included but the invitation excludes it.

### Example data

```text
From: Tom Reilly, site lead
Organization: Birch Siteworks, Cochrane
Date: 14 September 2026
Needed by: 30 September 2026

An estimate assumes night work is included but the invitation excludes it.

The scope basis: this decision only
Quantities they measured: Birch site, Cochrane. Stated in the ask, not documented anywhere else
Allowances: Two-week look-ahead and one other, both unconfirmed as of 14 September 2026
Exclusions: Birch site, Cochrane is open. Takeoff rev C was raised verbally and never logged
```

### Example outcome

**Assumption log**
To: Tom Reilly, site lead, Birch Siteworks
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Records the conflict and refuses to hide the exclusion.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The scope basis | this decision only | Needs confirmation |
| Quantities they measured | Birch site, Cochrane. Stated in the ask, not documented anywhere else | Carried into the draft |
| Allowances | Two-week look-ahead and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Exclusions | Birch site, Cochrane is open. Takeoff rev C was raised verbally and never logged | Needs confirmation |

**How this draft was built**

**1. State the documents the estimate is based on**

**2. List quantities as measured or as an allowance**

**3. Write exclusions plainly**

**4. Do not invent a productivity rate and call it fact. Label judgments**

**5. Note what a missing drawing would change**

**Deliberately not done**
- Hidden exclusions.
- Invented quantities.
- A log written to mislead.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Tom Reilly by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Hidden exclusions
- Invented quantities
- A log written to mislead

## Related skills

- `change-order`
- `proposal-writer`
