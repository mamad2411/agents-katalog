---
name: punch-list
description: "Turn a punch list into items with a location, an owner, and a done standard. Use when the user mentions punch list, snag list, deficiency list, closeout punch, or asks for a punch list. Construction skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: construction
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'punch-list' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Punch List

Turn a punch list into items with a location, an owner, and a done standard.

## When to use this skill

Use this skill when the user:

- punch list
- snag list
- deficiency list
- closeout punch

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

- The observed items
- Locations
- Responsible parties
- The done standard

## Workflow


### 1. Step 1

One item, one location, one owner.
### 2. Step 2

Describe the defect so someone can find it.
### 3. Step 3

Define done as observable, not as 'make good'.
### 4. Step 4

Separate life-safety items and say they are not cosmetic.
### 5. Step 5

Do not invent counts.
### 6. Step 6

Close an item only with evidence they accept.

## Output

Deliver a **punch list**.

- Purpose of this punch list, in two sentences.
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

Tom Reilly, site lead at Birch Siteworks in Cochrane, needs a punch list by 30 September 2026. A punch list says 'finish lobby' with no owner.

### Example data

```text
From: Tom Reilly, site lead
Organization: Birch Siteworks, Cochrane
Date: 14 September 2026
Needed by: 30 September 2026

A punch list says 'finish lobby' with no owner.

The observed items: Birch site, Cochrane, recorded 14 September 2026. No supporting file attached
Locations: Two-week look-ahead. Partly documented: the what is written down, the who is not
Responsible parties: Two-week look-ahead. Stated in the ask, not documented anywhere else
The done standard: their one-page rule dated 2 Mar 2026. No exception log since
```

### Example outcome

**Punch list**
To: Tom Reilly, site lead, Birch Siteworks
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A list of located items, with life-safety called out and an owner on each line.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The observed items | Birch site, Cochrane, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Locations | Two-week look-ahead. Partly documented: the what is written down, the who is not | Carried into the draft |
| Responsible parties | Two-week look-ahead. Stated in the ask, not documented anywhere else | Carried into the draft |
| The done standard | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |

**How this draft was built**

**1. One item, one location, one owner**

**2. Describe the defect so someone can find it**

**3. Define done as observable, not as 'make good'**

**4. Separate life-safety items and say they are not cosmetic**

**5. Do not invent counts**

**Deliberately not done**
- A vague make-good list.
- Life-safety mixed with paint nits.
- Closure without evidence.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Tom Reilly by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A vague make-good list
- Life-safety mixed with paint nits
- Closure without evidence

## Related skills

- `project-closeout`
- `nonconformance-report`
