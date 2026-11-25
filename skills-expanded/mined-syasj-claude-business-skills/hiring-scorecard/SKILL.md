---
name: hiring-scorecard
description: "Turn interview evidence into a hire, no-hire, or hold decision without a vibe vote. Use when the user mentions hiring scorecard, debrief, should we hire, candidate decision, or asks for a hiring scorecard. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'hiring-scorecard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Hiring Scorecard

Turn interview evidence into a hire, no-hire, or hold decision without a vibe vote.

## When to use this skill

Use this skill when the user:

- hiring scorecard
- debrief
- should we hire
- candidate decision

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

- The agreed criteria
- Evidence from each interviewer
- Concerns still open
- The decision owner

## Workflow


### 1. Use the criteria already set

Do not add a new must-have in the debrief to justify a preference.
### 2. Evidence over adjectives

'Great communication' needs the example the interviewer heard. Adjectives alone do not score.
### 3. Separate missing evidence from negative evidence

A short interview is not a failed answer.
### 4. Name the risk

The main way this hire could fail in the first six months, and whether a reference or work sample would reduce it.
### 5. Decide

Hire, no-hire, or hold for a specific missing fact. A hold needs a date.
### 6. Document fairly

The note should be something the company could show a reviewer. No jokes about candidates.

## Output

Deliver a **hiring scorecard**.

- Purpose of this hiring scorecard, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a hiring scorecard by 30 September 2026. The panel liked a candidate's energy but nobody tested the analysis outcome in the job description.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The panel liked a candidate's energy but nobody tested the analysis outcome in the job description.

The agreed criteria: their existing list, 6 lines. Two lines have no owner
Evidence from each interviewer: one PDF, 2 pages, dated 14 September 2026
Concerns still open: Jordan Hale and one other, both unconfirmed as of 14 September 2026
The decision owner: Chris Adeyemi, people lead
```

### Example outcome

**Hiring scorecard**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Marks that outcome untested and recommends a work sample instead of a hire.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Redline Parts | plan 130, actual 75 | Use | Both sides of the comparison are in the file |
| Lantern Inn | score 71 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Use the criteria already set
2. Evidence over adjectives
3. Separate missing evidence from negative evidence
4. Name the risk
5. Decide

**Deliberately not done**
- A vote based on who clicked with the founder.
- Moving the criteria after meeting a favorite.
- Undocumented side-channel vetoes.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Chris Adeyemi attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- A vote based on who clicked with the founder.
- Moving the criteria after meeting a favorite.
- Undocumented side-channel vetoes.

## Related skills

- `structured-interview`
- `offer-letter-checklist`
- `inclusive-hiring`
