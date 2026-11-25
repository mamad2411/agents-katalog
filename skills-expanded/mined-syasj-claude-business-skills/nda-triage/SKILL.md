---
name: nda-triage
description: "Triage a non-disclosure agreement so the user knows what it covers, how long, and what counsel should still check. Use when the user mentions review an NDA, non-disclosure agreement, mutual NDA, confidentiality agreement, or asks for a NDA triage note. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'nda-triage' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# NDA Triage

Triage a non-disclosure agreement so the user knows what it covers, how long, and what counsel should still check.

## When to use this skill

Use this skill when the user:

- review an NDA
- non-disclosure agreement
- mutual NDA
- confidentiality agreement

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

- The NDA text
- Who discloses what
- The purpose of the talks
- The user's non-negotiables, if any

## Workflow


### 1. Identify direction

Mutual or one-way, and whether that matches who will actually share information.
### 2. Purpose limit

What the recipient may do with the information, in the text's words.
### 3. Duration and residuals

How long duties last, and whether residual-memory language is present. Quote it if it is.
### 4. Exclusions

Standard exclusions only count if they appear in the text. Do not assume them.
### 5. Awkward clauses

Non-solicit, IP assignment, or exclusive dealing hidden in an NDA are flagged as out of place for counsel.
### 6. Recommend a path

Sign, ask counsel to review specific lines, or do not sign yet. This is a triage, not a clearance.

## Output

Deliver a **NDA triage note**.

- Purpose of this NDA triage note, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a NDA triage note by 30 September 2026. A partnership conversation came with a one-way NDA that also assigns IP improvements to the other side.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A partnership conversation came with a one-way NDA that also assigns IP improvements to the other side.

The NDA text: Harbor renewal, recorded 14 September 2026. No supporting file attached
Who discloses what: Elena Voss, operations lead
The purpose of the talks: A partnership conversation came with a one-way NDA that also assigns IP improvements to the other side. Stated once, in the ask. Not written down anywhere else
The user's non-negotiables, if any: Harbor renewal, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Nda triage note**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Flag the IP assignment as unexpected, quotes it, and sends that clause to counsel before signature.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The NDA text | Harbor renewal, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Who discloses what | Elena Voss, operations lead | Carried into the draft |
| The purpose of the talks | A partnership conversation came with a one-way NDA that also assigns IP improvements to the other side. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| The user's non-negotiables, if any | Harbor renewal, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Identify direction**  
Mutual or one-way, and whether that matches who will actually share information.

**2. Purpose limit**  
What the recipient may do with the information, in the text's words.

**3. Duration and residuals**  
How long duties last, and whether residual-memory language is present. Quote it if it is.

**4. Exclusions**  
Standard exclusions only count if they appear in the text. Do not assume them.

**5. Awkward clauses**  
Non-solicit, IP assignment, or exclusive dealing hidden in an NDA are flagged as out of place for counsel.

**Deliberately not done**
- Assuming mutual exclusions that are not in the file.
- Ignoring a non-solicit buried in the NDA.
- Declaring the NDA safe for every jurisdiction.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Assuming mutual exclusions that are not in the file.
- Ignoring a non-solicit buried in the NDA.
- Declaring the NDA safe for every jurisdiction.

## Related skills

- `contract-risk-review`
- `ip-ownership-checklist`
- `vendor-contract-playbook`
