---
name: marketing-claims-review
description: "Review marketing claims for substantiation gaps before they are published. Use when the user mentions marketing claims review, can we say this, substantiation, advertising review, or asks for a claims review note. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'marketing-claims-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Marketing Claims Review

Review marketing claims for substantiation gaps before they are published.

## When to use this skill

Use this skill when the user:

- marketing claims review
- can we say this
- substantiation
- advertising review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not legal advice and does not create an attorney-client relationship. Do not invent statutes, case names, or filing deadlines. Drafts are for qualified counsel in the relevant jurisdiction.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The draft claim
- The evidence they have
- Where it will appear
- The product the claim describes

## Workflow


### 1. Quote the claim

Review the words they will publish, not a softened retelling.
### 2. Match evidence

Each factual claim needs a source they possess. If the source is missing, the claim is not ready.
### 3. Watch absolutes

'Only', 'guaranteed', 'never', and performance numbers are high risk if evidence is thin. Recommend narrower wording.
### 4. Comparisons

Competitor comparisons need a fair basis they can show. Do not draft a comparison they cannot support.
### 5. Testimonials

Do not invent quotes. If they want a customer story, the customer must approve the real words.
### 6. Counsel for regulated claims

Health, safety, and financial-return claims are flagged, not cleared.

## Output

Deliver a **claims review note**.

- Purpose of this claims review note, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a claims review note by 30 September 2026. A landing page says the product cuts costs by 40 percent, and the only support is one customer's anecdote.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A landing page says the product cuts costs by 40 percent, and the only support is one customer's anecdote.

The draft claim: the draft sentence is broader than the note
The evidence they have: one PDF, 2 pages, dated 14 September 2026
Where it will appear: Contractor NDA, recorded 14 September 2026. No supporting file attached
The product the claim describes: the draft sentence is broader than the note
```

### Example outcome

**Claims review note**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks the percentage claim until evidence exists and offers narrower wording tied to that one story, clearly labeled.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The draft claim | the draft sentence is broader than the note | Needs confirmation |
| The evidence they have | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Where it will appear | Contractor NDA, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The product the claim describes | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Quote the claim**  
Review the words they will publish, not a softened retelling.

**2. Match evidence**  
Each factual claim needs a source they possess. If the source is missing, the claim is not ready.

**3. Watch absolutes**  
'Only', 'guaranteed', 'never', and performance numbers are high risk if evidence is thin. Recommend narrower wording.

**4. Comparisons**  
Competitor comparisons need a fair basis they can show. Do not draft a comparison they cannot support.

**5. Testimonials**  
Do not invent quotes. If they want a customer story, the customer must approve the real words.

**Deliberately not done**
- Inventing a statistic.
- Leaving 'guaranteed results' because it converts.
- Fake testimonials.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Inventing a statistic.
- Leaving 'guaranteed results' because it converts.
- Fake testimonials.

## Related skills

- `customer-story`
- `terms-of-service-outline`
- `positioning-statement`
