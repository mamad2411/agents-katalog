---
name: sustainability-claim-review
description: "Review a sustainability claim for substantiation before it is published. Use when the user mentions sustainability claim, green claim, ESG claim review, net zero wording, or asks for a claim review. Sustainability skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sustainability
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sustainability-claim-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sustainability Claim Review

Review a sustainability claim for substantiation before it is published.

## When to use this skill

Use this skill when the user:

- sustainability claim
- green claim
- ESG claim review
- net zero wording

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent emissions factors or certification status. Label estimates. This is not an assurance opinion.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The claim
- The evidence
- Where it will appear
- The reviewer

## Workflow


### 1. Step 1

Quote the claim.
### 2. Step 2

Match each factual part to evidence.
### 3. Step 3

Qualifiers such as net zero or carbon neutral need the basis they can show. If the basis is missing, cut the words.
### 4. Step 4

Avoid vague 'eco' language that implies a standard they do not meet.
### 5. Step 5

Send legal and advertising questions to counsel if they said the jurisdiction requires it.
### 6. Step 6

Do not help greenwash.

## Output

Deliver a **claim review**.

- Purpose of this claim review, in two sentences.
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

Devon Hale, reporting lead at Prairie Line Energy in Calgary, needs a claim review by 30 September 2026. Packaging says 'carbon neutral' and the only support is an intention.

### Example data

```text
From: Devon Hale, reporting lead
Organization: Prairie Line Energy, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Packaging says 'carbon neutral' and the only support is an intention.

The claim: the draft sentence is broader than the note
The evidence: one PDF, 2 pages, dated 14 September 2026
Where it will appear: Emissions factor sheet, recorded 14 September 2026. No supporting file attached
The reviewer: Devon Hale. No second reviewer named
```

### Example outcome

**Claim review**
To: Devon Hale, reporting lead, Prairie Line Energy
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the phrase until the basis exists.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The claim | the draft sentence is broader than the note | Needs confirmation |
| The evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Where it will appear | Emissions factor sheet, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The reviewer | Devon Hale. No second reviewer named | Needs confirmation |

**How this draft was built**

**1. Quote the claim**

**2. Match each factual part to evidence**

**3. Qualifiers such as net zero or carbon neutral need the basis they can show. If the basis is missing, cut the words**

**4. Avoid vague 'eco' language that implies a standard they do not meet**

**5. Send legal and advertising questions to counsel if they said the jurisdiction requires it**

**Deliberately not done**
- Greenwashing.
- A standard implied but not held.
- A claim with no evidence.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Devon Hale by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Greenwashing
- A standard implied but not held
- A claim with no evidence

## Related skills

- `marketing-claims-review`
- `emissions-inventory-brief`
