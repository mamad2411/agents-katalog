---
name: compensation-band
description: "Review a pay decision against the band and the evidence, without inventing market rates. Use when the user mentions pay band, compensation review, salary band, offer versus band, or asks for a compensation review note. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'compensation-band' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Compensation Band Review

Review a pay decision against the band and the evidence, without inventing market rates.

## When to use this skill

Use this skill when the user:

- pay band
- compensation review
- salary band
- offer versus band

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The band if they have one
- The proposed pay
- The evidence for the person's level
- Internal peers the user chooses to include

## Workflow


### 1. Start with their band

If no band exists, say the decision is discretionary and do not invent market percentiles.
### 2. Level evidence

Does the person's work match the level definition they provided. Pay does not define level after the fact.
### 3. Internal consistency

Compare only with peers the user supplied. Do not guess what others are paid.
### 4. Range placement

Where the proposal sits in the band, and what would justify an exception.
### 5. Exception log

If they go outside the band, name the approver and the review date.
### 6. No market theater

You may list questions for a compensation consultant. You do not fabricate a survey number.

## Output

Deliver a **compensation review note**.

- Purpose of this compensation review note, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a compensation review note by 30 September 2026. A manager wants to beat a competitor's verbal offer and the proposal sits above the band.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants to beat a competitor's verbal offer and the proposal sits above the band.

The band if they have one: Jordan Hale, recorded 14 September 2026. No supporting file attached
The proposed pay: Jordan Hale, recorded 14 September 2026. No supporting file attached
The evidence for the person's level: one PDF, 2 pages, dated 14 September 2026
Internal peers the user chooses to include: Sam Okonkwo. Stated in the ask, not documented anywhere else
```

### Example outcome

**Compensation review note**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Places the proposal above the band, requires an approver, and does not invent a market percentile.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The band if they have one | Jordan Hale, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The proposed pay | Jordan Hale, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The evidence for the person's level | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Internal peers the user chooses to include | Sam Okonkwo. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Start with their band**  
If no band exists, say the decision is discretionary and do not invent market percentiles.

**2. Level evidence**  
Does the person's work match the level definition they provided. Pay does not define level after the fact.

**3. Internal consistency**  
Compare only with peers the user supplied. Do not guess what others are paid.

**4. Range placement**  
Where the proposal sits in the band, and what would justify an exception.

**5. Exception log**  
If they go outside the band, name the approver and the review date.

**Deliberately not done**
- Invented percentile data.
- A raise justified only by a competing anecdote with no band.
- Comparing to peers the user did not authorize you to discuss.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented percentile data.
- A raise justified only by a competing anecdote with no band.
- Comparing to peers the user did not authorize you to discuss.

## Related skills

- `offer-letter-checklist`
- `total-rewards-brief`
- `workforce-plan`
