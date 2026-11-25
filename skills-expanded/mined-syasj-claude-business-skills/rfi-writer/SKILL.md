---
name: rfi-writer
description: "Write a request for information that states the conflict, the location, and the date the answer is needed. Use when the user mentions RFI, request for information, drawing conflict, design clarification, or asks for a RFI. Construction skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: construction
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'rfi-writer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# RFI Writer

Write a request for information that states the conflict, the location, and the date the answer is needed.

## When to use this skill

Use this skill when the user:

- RFI
- request for information
- drawing conflict
- design clarification

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

- The conflict
- The drawing or spec location
- The date needed
- The proposed clarification if any

## Workflow


### 1. Step 1

Describe the conflict with locations they gave.
### 2. Step 2

Ask one question.
### 3. Step 3

State the date the answer is needed and why.
### 4. Step 4

A proposed clarification is labeled as a proposal, not as approval.
### 5. Step 5

Attach references they have. Do not invent a detail.
### 6. Step 6

Track the RFI so work does not proceed on a guess unless they accept that risk in writing.

## Output

Deliver a **RFI**.

- Purpose of this RFI, in two sentences.
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

Tom Reilly, site lead at Birch Siteworks in Cochrane, needs a RFI by 30 September 2026. An RFI asks the designer to 'see the attached and advise' with no question.

### Example data

```text
From: Tom Reilly, site lead
Organization: Birch Siteworks, Cochrane
Date: 14 September 2026
Needed by: 30 September 2026

An RFI asks the designer to 'see the attached and advise' with no question.

The conflict: Birch site, Cochrane, recorded 14 September 2026. No supporting file attached
The drawing or spec location: two deals cited from memory. Neither has a written loss reason
The date needed: 30 September 2026
The proposed clarification if any: Birch site, Cochrane, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Rfi**
To: Tom Reilly, site lead, Birch Siteworks
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
An RFI with one located question, a need-by date, and no invented detail.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The conflict | Birch site, Cochrane, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The drawing or spec location | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| The date needed | 30 September 2026 | Carried into the draft |
| The proposed clarification if any | Birch site, Cochrane, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Describe the conflict with locations they gave**

**2. Ask one question**

**3. State the date the answer is needed and why**

**4. A proposed clarification is labeled as a proposal, not as approval**

**5. Attach references they have. Do not invent a detail**

**Deliberately not done**
- Three questions in one RFI.
- An invented detail.
- Work proceeding on a silent guess.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Tom Reilly by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Three questions in one RFI
- An invented detail
- Work proceeding on a silent guess

## Related skills

- `change-order`
- `site-daily-report`
