---
name: supplier-sustainability-questionnaire
description: "Review supplier sustainability answers for evidence, not for a score that hides missing proof. Use when the user mentions supplier sustainability, ESG questionnaire, supplier carbon data, sustainability survey review, or asks for a questionnaire review. Sustainability skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sustainability
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'supplier-sustainability-questionnaire' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Supplier Sustainability Questionnaire

Review supplier sustainability answers for evidence, not for a score that hides missing proof.

## When to use this skill

Use this skill when the user:

- supplier sustainability
- ESG questionnaire
- supplier carbon data
- sustainability survey review

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

- The questions
- The answers
- Evidence attached
- The decision the score would feed

## Workflow


### 1. Step 1

Score evidence, not adjectives.
### 2. Step 2

A missing answer is a gap, not a zero that looks precise.
### 3. Step 3

Do not invent a supplier's emissions.
### 4. Step 4

Note claims of certification only if the certificate is in the file.
### 5. Step 5

Recommend follow-up questions.
### 6. Step 6

Do not use the questionnaire to accuse a supplier of fraud. Ask for evidence.

## Output

Deliver a **questionnaire review**.

- Purpose of this questionnaire review, in two sentences.
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

Devon Hale, reporting lead at Prairie Line Energy in Calgary, needs a questionnaire review by 30 September 2026. A supplier says it is certified and attaches no certificate.

### Example data

```text
From: Devon Hale, reporting lead
Organization: Prairie Line Energy, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A supplier says it is certified and attaches no certificate.

The questions: A supplier says it is certified and attaches no certificate
The answers: Scope 2 electricity, recorded 14 September 2026. No supporting file attached
Evidence attached: one PDF, 2 pages, dated 14 September 2026
The decision the score would feed: CAD 180, from their sheet, not a guess
```

### Example outcome

**Questionnaire review**
To: Devon Hale, reporting lead, Prairie Line Energy
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Marks the certification unverified and asks for the document.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The questions | A supplier says it is certified and attaches no certificate | Needs confirmation |
| The answers | Scope 2 electricity, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Evidence attached | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The decision the score would feed | CAD 180, from their sheet, not a guess | Needs confirmation |

**How this draft was built**

**1. Score evidence, not adjectives**

**2. A missing answer is a gap, not a zero that looks precise**

**3. Do not invent a supplier's emissions**

**4. Note claims of certification only if the certificate is in the file**

**5. Recommend follow-up questions**

**Deliberately not done**
- An invented supplier footprint.
- A certification assumed.
- A precise score on missing data.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Devon Hale by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An invented supplier footprint
- A certification assumed
- A precise score on missing data

## Related skills

- `supplier-scorecard`
- `vendor-security-review`
